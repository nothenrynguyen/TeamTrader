# NHL Trade Validation

A Django + Tailwind web app for validating NHL trades based on salary cap, roster rules, and retained salary limits.

## Current Features
- Django project setup with Tailwind CSS
- Models for Teams, Contracts, Draft Picks, Retained Salaries
- CSV data loaders for NHL roster and contract information

## Getting Started
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py load_data
python manage.py load_retention trades\data\retention_used.csv
python manage.py runserver
