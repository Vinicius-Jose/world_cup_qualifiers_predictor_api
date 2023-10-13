from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .service import AI
from .models import Team, Match
from .serializers import TeamSerializer, MatchSerializer


# Create your views here.
class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Team to be viewed or edited.
    """

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "id"]
    filterset_fields = ["name", "id"]


class MatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Match to be viewed or edited.
    """

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["id", "home_team", "away_team"]
    filterset_fields = ["name", "id"]


@api_view(["POST"])
def predict_match(request: Request, home_team: Team, away_team: Team) -> Response:
    match = Match(home_team=home_team, away_team=away_team)
    ai = AI()
    result = {
        "home_team": TeamSerializer(home_team),
        "away_team": TeamSerializer(away_team),
        "home_team_victory": 0,
        "away_team_victory": 0,
        "draw": 0,
    }
    if ai.load():
        probs = ai.evaluate(match.to_tensor())
        result.update(
            {
                "home_team_victory": probs[0].item(),
                "away_team_victory": probs[1].item(),
                "draw": probs[2].item(),
            }
        )
    return Response(result, status=status.HTTP_200_OK)
