from django.core.management.base import BaseCommand
from trades.models import DraftPick, Team
import pandas as pd


class Command(BaseCommand):
    help = "Load draft picks from draft_picks.csv"

    def handle(self, *args, **kwargs):
        file_path = 'trades/data/draft_picks.csv'
        df = pd.read_csv(file_path)

        count = 0
        for _, row in df.iterrows():
            team_abbr = row['team_abbrv']
            try:
                team = Team.objects.get(abbr=team_abbr)
            except Team.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Team not found: {team_abbr}"))
                continue

            DraftPick.objects.create(
                owning_team=team,
                year=row['year'],
                rnd=row['round'],
                # original_team_abbr and overall not provided
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded {count} draft picks"))
