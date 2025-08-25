import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradebot.settings')
django.setup()

from trades.models import Team

csv_path = os.path.join('trades', 'data', 'teams.csv')

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name'].strip()
        abbr = row['abbreviation'].strip()

        team, created = Team.objects.get_or_create(abbr=abbr, defaults={"name": name})
        if created:
            print(f"Created team: {abbr}")
        else:
            print(f"Already exists: {abbr}")
