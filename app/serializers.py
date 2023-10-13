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
    winner = serializers.SerializerMethodField("get_winner")

    def get_winner(self, obj: Match):
        if obj.winner:
            return Team.objects.get(id=obj.winner)
        elif obj.winner == -1:
            return "Empate"
        return None

    class Meta:
        model = Match
        fields = [
            "id",
            "home_team",
            "away_team",
            "winner",
        ]
