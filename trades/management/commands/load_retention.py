from django.core.management.base import BaseCommand
import csv
from trades.models import Team, RetainedSalary

class Command(BaseCommand):
    help = "Load retained salary rows from a CSV with flexible headers"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **opts):
        path = opts["csv_path"]
        count = 0

        with open(path, "r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(2048)
            f.seek(0)

            # Detect delimiter (comma/semicolon/tab)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except Exception:
                dialect = csv.excel
            reader = csv.reader(f, dialect)

            # Read headers and find columns by fuzzy name match
            headers = [h.strip().lower() for h in next(reader)]
            def find_idx(options):
                for i, h in enumerate(headers):
                    for opt in options:
                        if h == opt or opt in h:
                            return i
                return None

            team_i   = find_idx(["team_abbrv", "team_abbrev", "team", "abbr"])
            season_i = find_idx(["season", "season_year", "year"])
            player_i = find_idx(["player_name", "player"])

            if team_i is None or season_i is None or player_i is None:
                self.stdout.write(self.style.WARNING(
                    f"Could not detect columns. Headers found: {headers}"
                ))
                return

            for row in reader:
                try:
                    abbr = (row[team_i] or "").strip()
                    season = (row[season_i] or "").strip()
                    player = (row[player_i] or "").strip()
                except IndexError:
                    continue
                if not abbr or not season or not player:
                    continue

                team, _ = Team.objects.get_or_create(abbr=abbr)
                RetainedSalary.objects.update_or_create(
                    team=team, season=season, player_name=player
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Loaded/updated {count} retained-salary rows from {path}"
        ))
