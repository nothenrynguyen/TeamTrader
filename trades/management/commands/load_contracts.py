from django.core.management.base import BaseCommand
import pandas as pd
from trades.models import Contract

class Command(BaseCommand):
    help = 'Load player contracts from contracts.csv'

    def handle(self, *args, **kwargs):
        file_path = 'data/contracts.csv'
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            Contract.objects.create(
                player_name=row['player_name'],
                team=row['team'],
                position=row['position'],
                cap_hit=row['cap_hit'],
                term_remaining=row['term_remaining']
            )

        self.stdout.write(self.style.SUCCESS(f"Loaded {len(df)} contracts"))
