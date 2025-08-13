from django.core.management.base import BaseCommand
import pandas as pd
from trades.models import DraftPick

class Command(BaseCommand):
    help = 'Load draft picks from draft_picks.csv'

    def handle(self, *args, **kwargs):
        file_path = 'data/draft_picks.csv'
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            DraftPick.objects.create(
                year=row['year'],
                round=row['round'],
                team=row['team'],
                original_owner=row['original_owner']
            )

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(df)} draft picks"))
