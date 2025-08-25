from django.core.management.base import BaseCommand
from trades.models import RetainedSalary, Team
import pandas as pd


class Command(BaseCommand):
    help = "Load retained salaries from retention_used.csv"

    def handle(self, *args, **kwargs):
        file_path = 'trades/data/retention_used.csv'
        df = pd.read_csv(file_path)

        count = 0
        for _, row in df.iterrows():
            team_abbr = row.get('team_abbrv')
            if not team_abbr:
                continue

            try:
                team = Team.objects.get(abbr=team_abbr)
            except Team.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Team not found: {team_abbr}"))
                continue

            RetainedSalary.objects.create(
                team=team,
                season=row['season'],
                player_name=row['player_name']
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded {count} retained salary entries"))
