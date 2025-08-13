from django.core.management.base import BaseCommand
import csv
from trades.models import Team, Contract, DraftPick, RetainedSalary
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

class Command(BaseCommand):
    help = "Load initial data from CSV files"

    def handle(self, *args, **kwargs):
        self.load_teams()
        self.load_contracts()
        self.load_draft_picks()
        self.load_retained_salaries()

    def load_teams(self):
        # We’ll extract team abbreviations from the other CSVs automatically
        team_abbrs = set()

        # From contracts.csv
        with open(DATA_DIR / "contracts.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("team_abbrv"):
                    team_abbrs.add(row["team_abbrv"])
                if row.get("nhl_rights_abbrv"):
                    team_abbrs.add(row["nhl_rights_abbrv"])

        # From draft_picks.csv
        with open(DATA_DIR / "draft_picks.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("owning_team_abbr"):
                    team_abbrs.add(row["owning_team_abbr"])
                if row.get("original_team_abbr"):
                    team_abbrs.add(row["original_team_abbr"])

        # From retention_used.csv
        with open(DATA_DIR / "retention_used.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("team_abbrv"):
                    team_abbrs.add(row["team_abbrv"])

        for abbr in sorted(team_abbrs):
            if abbr:
                Team.objects.get_or_create(abbr=abbr)

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(team_abbrs)} teams"))

    def load_contracts(self):
        with open(DATA_DIR / "contracts.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            created = 0
            for row in reader:
                team = Team.objects.filter(abbr=row.get("team_abbrv")).first()

                # normalize helpers
                def to_int(x):
                    try:
                        return int(float(str(x).replace(",", "").replace("$", "")))
                    except Exception:
                        return None

                def to_bool(x):
                    s = str(x).strip().lower()
                    return s in {"1", "true", "t", "yes", "y"}

                defaults = {
                    "full_name": row.get("full_name"),
                    "position": row.get("position"),
                    "dob": row.get("dob"),
                    "height": row.get("height"),
                    "weight": row.get("weight"),
                    "shoots": row.get("shoots"),
                    "nhl_rights": row.get("nhl_rights"),
                    "nhl_rights_abbrv": row.get("nhl_rights_abbrv"),
                    "team": team,
                    "contract_type": row.get("contract_type"),
                    "contract_length": to_int(row.get("contract_length")),
                    "years_remaining": to_int(row.get("years_remaining")),
                    "last_season": row.get("last_season"),
                    "contract_value": to_int(row.get("contract_value")),
                    "cap_hit": to_int(row.get("cap_hit")),
                    "expiry_status": row.get("expiry_status"),
                    "clause_details": row.get("clause_details"),
                    "waivers_eligible": row.get("waivers_eligible"),
                    "exclude_50contract": to_bool(row.get("exclude_50contract")),
                    "active": to_bool(row.get("active", "true")),
                }

                nhl_id = row.get("nhl_id") or None
                full_name = row.get("full_name") or ""

                # Upsert using whatever id we have (id + name gives us stability if id is missing)
                obj, _ = Contract.objects.update_or_create(
                    nhl_id=nhl_id, full_name=full_name, defaults=defaults
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Contracts loaded/updated: {created}"))


    def load_draft_picks(self):
        with open(DATA_DIR / "draft_picks.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            created = 0

            def to_int(x):
                try:
                    return int(str(x).strip())
                except Exception:
                    return None

            for row in reader:
                owning_abbr = (
                    row.get("owning_team_abbr")
                    or row.get("team_abbrv")
                    or row.get("team")
                    or row.get("owning_team")
                    or ""
                ).strip()

                # If original team missing, fall back to owning
                original_abbr = (
                    row.get("original_team_abbr")
                    or row.get("original_team")
                    or row.get("from_team")
                    or owning_abbr
                    or ""
                ).strip()

                year = to_int(row.get("year") or row.get("season_year"))
                rnd = to_int(row.get("round") or row.get("rnd"))
                overall = to_int(row.get("overall"))

                # minimal required fields
                if not owning_abbr or not year or not rnd:
                    continue

                owning_team = Team.objects.filter(abbr=owning_abbr).first()
                if not owning_team:
                    owning_team, _ = Team.objects.get_or_create(abbr=owning_abbr)

                obj, _ = DraftPick.objects.update_or_create(
                    owning_team=owning_team,
                    original_team_abbr=original_abbr or None,
                    year=year,
                    rnd=rnd,
                    defaults={"overall": overall},
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Draft picks loaded/updated: {created}"))


    def load_retained_salaries(self):
        with open(DATA_DIR / "retention_used.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                team = Team.objects.filter(abbr=row.get("team_abbrv")).first()
                RetainedSalary.objects.create(
                    team=team,
                    season=row.get("season"),
                    player_name=row.get("player_name")
                )
        self.stdout.write(self.style.SUCCESS("Retained salaries loaded"))
