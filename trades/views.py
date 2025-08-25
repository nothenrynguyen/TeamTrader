from django.shortcuts import render
from trades.models import Team, Contract, DraftPick, RetainedSalary

# NHL team display mapping
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

    team_a = Team.objects.filter(abbr=team_a_code).first()
    team_b = Team.objects.filter(abbr=team_b_code).first()

    team_a_players = Contract.objects.filter(team=team_a) if team_a else []
    team_b_players = Contract.objects.filter(team=team_b) if team_b else []

    team_a_picks = DraftPick.objects.filter(owning_team=team_a).order_by("year", "rnd") if team_a else []
    team_b_picks = DraftPick.objects.filter(owning_team=team_b).order_by("year", "rnd") if team_b else []

    team_a_retained = RetainedSalary.objects.filter(team=team_a).order_by("season") if team_a else []
    team_b_retained = RetainedSalary.objects.filter(team=team_b).order_by("season") if team_b else []

    return render(request, "index.html", {
        "teams": TEAMS.values(),
        "team_a": team_a,
        "team_b": team_b,
        "team_a_players": team_a_players,
        "team_b_players": team_b_players,
        "team_a_picks": team_a_picks,
        "team_b_picks": team_b_picks,
        "team_a_retained": team_a_retained,
        "team_b_retained": team_b_retained,
    })

