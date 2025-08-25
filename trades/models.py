from django.db import models


class Team(models.Model):
    abbr = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=64, blank=True, default="")

    def __str__(self):
        return self.abbr


class Contract(models.Model):
    """
    One row per player contract line from contracts.csv.
    """
    nhl_id = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    full_name = models.CharField(max_length=128)
    position = models.CharField(max_length=8, blank=True, default="")
    dob = models.CharField(max_length=32, blank=True, default="")  # keep string if not normalized
    height = models.CharField(max_length=16, blank=True, default="")
    weight = models.CharField(max_length=16, blank=True, default="")
    shoots = models.CharField(max_length=8, blank=True, default="")

    nhl_rights = models.CharField(max_length=64, blank=True, default="")
    nhl_rights_abbrv = models.CharField(max_length=5, blank=True, default="")

    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name="contracts")

    contract_type = models.CharField(max_length=32, blank=True, default="")
    contract_length = models.IntegerField(null=True, blank=True)
    years_remaining = models.IntegerField(null=True, blank=True)
    last_season = models.CharField(max_length=16, blank=True, default="")
    contract_value = models.BigIntegerField(null=True, blank=True)
    cap_hit = models.BigIntegerField(null=True, blank=True)
    expiry_status = models.CharField(max_length=32, blank=True, default="")
    clause_details = models.CharField(max_length=256, blank=True, default="")
    waivers_eligible = models.CharField(max_length=16, blank=True, default="")
    exclude_50contract = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} ({self.nhl_rights_abbrv or self.team_id})"


class DraftPick(models.Model):
    """
    One row per pick in draft_picks.csv.
    """
    owning_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="picks_owned")
    original_team_abbr = models.CharField(max_length=5, blank=True, null=True)
    year = models.IntegerField()
    rnd = models.IntegerField()
    overall = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.owning_team.abbr} {self.year} R{self.rnd}"


class RetainedSalary(models.Model):
    """
    One row per retained salary case from retention_used.csv.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="retentions")
    season = models.CharField(max_length=16)
    player_name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.team.abbr} retains {self.player_name} ({self.season})"
