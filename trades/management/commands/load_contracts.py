from django.core.management.base import BaseCommand
import pandas as pd
from trades.models import Contract, Team

class Command(BaseCommand):
    help = 'Load player contracts from contracts.csv'

    def handle(self, *args, **kwargs):
        file_path = 'trades/data/contracts.csv'
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            team_abbr = row.get('nhl_rights_abbrv')
            team = Team.objects.filter(abbr=team_abbr).first()

            Contract.objects.create(
                nhl_id=row.get('nhl_id'),
                full_name=row.get('full_name'),
                position=row.get('position'),
                dob=row.get('dob'),
                height=row.get('height'),
                weight=row.get('weight'),
                shoots=row.get('shoots'),
                nhl_rights=row.get('nhl_rights'),
                nhl_rights_abbrv=team_abbr,
                team=team,
                contract_type=row.get('contract_type'),
                contract_length=int(row['contract_length']) if pd.notna(row['contract_length']) else None,
                years_remaining=int(row['years_remaining']) if pd.notna(row['years_remaining']) else None,
                last_season=row.get('last_season'),
                contract_value=int(row['contract_value']) if pd.notna(row['contract_value']) else None,
                cap_hit=int(row['cap_hit']) if pd.notna(row['cap_hit']) else None,
                expiry_status=row.get('expiry_status'),
                clause_details=row.get('clause_details'),
                waivers_eligible=row.get('waivers_eligible'),
                exclude_50contract=row.get('exclude_50contract') == True or row.get('exclude_50contract') == "TRUE",
                active=row.get('active') == True or row.get('active') == "TRUE",
            )

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(df)} contracts"))
