from django.shortcuts import render
import pandas as pd
import os
from django.conf import settings

BASE_DIR = settings.BASE_DIR

# Full NHL team mapping
TEAMS = {
    "ANA": {"code": "ANA", "name": "Anaheim Ducks"},
    "ARI": {"code": "ARI", "name": "Arizona Coyotes"},
    "BOS": {"code": "BOS", "name": "Boston Bruins"},
    "BUF": {"code": "BUF", "name": "Buffalo Sabres"},
    "CGY": {"code": "CGY", "name": "Calgary Flames"},
    "CAR": {"code": "CAR", "name": "Carolina Hurricanes"},
    "CHI": {"code": "CHI", "name": "Chicago Blackhawks"},
    "COL": {"code": "COL", "name": "Colorado Avalanche"},
    "CBJ": {"code": "CBJ", "name": "Columbus Blue Jackets"},
    "DAL": {"code": "DAL", "name": "Dallas Stars"},
    "DET": {"code": "DET", "name": "Detroit Red Wings"},
    "EDM": {"code": "EDM", "name": "Edmonton Oilers"},
    "FLA": {"code": "FLA", "name": "Florida Panthers"},
    "LAK": {"code": "LAK", "name": "Los Angeles Kings"},
    "MIN": {"code": "MIN", "name": "Minnesota Wild"},
    "MTL": {"code": "MTL", "name": "Montréal Canadiens"},
    "NSH": {"code": "NSH", "name": "Nashville Predators"},
    "NJD": {"code": "NJD", "name": "New Jersey Devils"},
    "NYI": {"code": "NYI", "name": "New York Islanders"},
    "NYR": {"code": "NYR", "name": "New York Rangers"},
    "OTT": {"code": "OTT", "name": "Ottawa Senators"},
    "PHI": {"code": "PHI", "name": "Philadelphia Flyers"},
    "PIT": {"code": "PIT", "name": "Pittsburgh Penguins"},
    "SJS": {"code": "SJS", "name": "San Jose Sharks"},
    "SEA": {"code": "SEA", "name": "Seattle Kraken"},
    "STL": {"code": "STL", "name": "St. Louis Blues"},
    "TBL": {"code": "TBL", "name": "Tampa Bay Lightning"},
    "TOR": {"code": "TOR", "name": "Toronto Maple Leafs"},
    "VAN": {"code": "VAN", "name": "Vancouver Canucks"},
    "VGK": {"code": "VGK", "name": "Vegas Golden Knights"},
    "WSH": {"code": "WSH", "name": "Washington Capitals"},
    "WPG": {"code": "WPG", "name": "Winnipeg Jets"},
}

def index(request):
    team_a_code = request.GET.get("team_a")
    team_b_code = request.GET.get("team_b")

    # Load contracts.csv from the correct path
    contracts_path = os.path.join(BASE_DIR, "trades", "data", "contracts.csv")
    contracts_df = pd.read_csv(contracts_path)

    # Filter player data by team
    team_a_players = contracts_df[contracts_df["nhl_rights_abbrv"] == team_a_code].to_dict("records") if team_a_code else []
    team_b_players = contracts_df[contracts_df["nhl_rights_abbrv"] == team_b_code].to_dict("records") if team_b_code else []

    # Get team objects (name + code)
    team_a = TEAMS.get(team_a_code)
    team_b = TEAMS.get(team_b_code)

    return render(request, "index.html", {
        "teams": TEAMS.values(),
        "team_a": team_a,
        "team_b": team_b,
        "team_a_players": team_a_players,
        "team_b_players": team_b_players,
    })
