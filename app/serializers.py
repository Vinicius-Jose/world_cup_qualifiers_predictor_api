from rest_framework import serializers
from .models import Team, Match
from .service import AI


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]


class MatchSerializer(serializers.ModelSerializer):
    home_team = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Team.objects.all()
    )
    away_team = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Team.objects.all()
    )
    winner = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Team.objects.all()
    )  # If the value is null means it was a draw match

    class Meta:
        model = Match
        fields = [
            "id",
            "home_team",
            "away_team",
            "winner",
        ]


class PredictSerializer(serializers.ModelSerializer):
    home_team = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Team.objects.all()
    )
    away_team = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=Team.objects.all()
    )
    probs = serializers.SerializerMethodField(
        method_name=("get_probs")
    )  # If the value is null means it was a draw match

    def get_probs(self, match: dict):
        ai = AI()
        match = Match(**match)
        result = {
            "home_team": match.home_team.name,
            "away_team": match.away_team.name,
            "home_team_victory": 0,
            "away_team_victory": 0,
            "draw": 0,
        }

        if ai.load(save_path="app/data/torch/teams_ai_api.chkpt"):
            probs = ai.evaluate(match.to_tensor())
            result.update(
                {
                    "home_team_victory": probs[0].item(),
                    "away_team_victory": probs[1].item(),
                    "draw": probs[2].item(),
                }
            )
        return result

    class Meta:
        model = Match
        fields = ["id", "home_team", "away_team", "probs"]
