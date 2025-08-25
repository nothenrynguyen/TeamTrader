from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Team, Contract, DraftPick, RetainedSalary
import json

@csrf_exempt
@require_POST
def validate_trade(request):
    try:
        data = json.loads(request.body)
        code_a = data.get("team_a")
        code_b = data.get("team_b")
        errors = []

        if not code_a or not code_b:
            return JsonResponse({"errors": ["Missing team codes."]}, status=400)

        try:
            team_a = Team.objects.get(abbr=code_a)
            team_b = Team.objects.get(abbr=code_b)
        except Team.DoesNotExist:
            return JsonResponse({"errors": ["One or both team codes are invalid."]}, status=400)

        # extract selected asset IDs from payload
        team_a_players = data.get("team_a_players", [])
        team_a_picks = data.get("team_a_picks", [])
        team_a_retained = data.get("team_a_retained", [])

        team_b_players = data.get("team_b_players", [])
        team_b_picks = data.get("team_b_picks", [])
        team_b_retained = data.get("team_b_retained", [])

        # validate ownership of each asset
        for pid in team_a_players:
            if not Contract.objects.filter(id=pid, team=team_a).exists():
                errors.append(f"{team_a.name} does not own player with ID {pid}.")

        for pid in team_b_players:
            if not Contract.objects.filter(id=pid, team=team_b).exists():
                errors.append(f"{team_b.name} does not own player with ID {pid}.")

        for pick_id in team_a_picks:
            if not DraftPick.objects.filter(id=pick_id, owning_team=team_a).exists():
                errors.append(f"{team_a.name} does not own draft pick ID {pick_id}.")

        for pick_id in team_b_picks:
            if not DraftPick.objects.filter(id=pick_id, owning_team=team_b).exists():
                errors.append(f"{team_b.name} does not own draft pick ID {pick_id}.")

        for rid in team_a_retained:
            if not RetainedSalary.objects.filter(id=rid, team=team_a).exists():
                errors.append(f"{team_a.name} does not control retained salary ID {rid}.")

        for rid in team_b_retained:
            if not RetainedSalary.objects.filter(id=rid, team=team_b).exists():
                errors.append(f"{team_b.name} does not control retained salary ID {rid}.")

        # check that each team is offering at least 1 asset
        if not (team_a_players or team_a_picks or team_a_retained):
            errors.append(f"{team_a.name} must offer at least one player, pick, or retained salary.")
        if not (team_b_players or team_b_picks or team_b_retained):
            errors.append(f"{team_b.name} must offer at least one player, pick, or retained salary.")

        # calculate cap hits only for players being traded
        cap_a = sum([c.cap_hit or 0 for c in Contract.objects.filter(id__in=team_a_players)])
        cap_b = sum([c.cap_hit or 0 for c in Contract.objects.filter(id__in=team_b_players)])
        cap_diff = abs(cap_a - cap_b)

        if cap_diff > 5_000_000:
            errors.append(
                f"Cap hit difference (${cap_diff:,.0f}) exceeds the $5M threshold.\n"
                f"{team_a.name} selected player cap hit: ${cap_a:,.0f} | {team_b.name} selected player cap hit: ${cap_b:,.0f}"
            )

        if errors:
            return JsonResponse({"errors": errors}, status=200)

        # no errors
        summary = (
            f"Trade between {team_a.name} and {team_b.name} is valid.\n"
            f"{team_a.name} sending {len(team_a_players)} player(s), {len(team_a_picks)} pick(s), "
            f"and {len(team_a_retained)} retained salary item(s).\n"
            f"{team_b.name} sending {len(team_b_players)} player(s), {len(team_b_picks)} pick(s), "
            f"and {len(team_b_retained)} retained salary item(s)."
        )
        return JsonResponse({"message": summary, "errors": []})

    except Exception as e:
        return JsonResponse({"errors": [f"Server error: {str(e)}"]}, status=500)

@csrf_exempt
def load_rosters(request):
    team_a_code = request.GET.get("team_a")
    team_b_code = request.GET.get("team_b")

    def get_team_data(team_code):
        team = Team.objects.filter(abbr=team_code).first()
        return {
            "name": team.name if team else team_code,
            "players": list(Contract.objects.filter(team=team).values("id", "full_name", "position")),
            "picks": list(DraftPick.objects.filter(owning_team=team).values("id", "year", "rnd")),
            "retained": list(RetainedSalary.objects.filter(team=team).values("id", "player_name", "season"))
        }

    return JsonResponse({
        "team_a": get_team_data(team_a_code),
        "team_b": get_team_data(team_b_code)
    })
