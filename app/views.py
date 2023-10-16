from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Team, Match
from .serializers import TeamSerializer, MatchSerializer, PredictSerializer
import json
from torch.utils.data import DataLoader, Dataset
import torch
from .service import AI


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
    filterset_fields = ["home_team", "id"]


class PredictMatchViewSet(viewsets.ViewSet):
    serializer_class = PredictSerializer
    queryset = Match.objects.all()

    def post(self, request: Request) -> Response:
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            dados_json = renderers.JSONRenderer().render(serializer.data)

        return Response(
            json.loads(dados_json), status=200, content_type="application/json"
        )

    def get(self, request: Request) -> Response:
        dataset = Data()
        data_loader = DataLoader(dataset=dataset, batch_size=2)
        ai = AI()
        total_loss = ai.train(epochs=20, data_loader=data_loader)
        ai.save(save_path="app/data/torch/teams_ai_api.chkpt")
        dados_json = renderers.JSONRenderer().render({"loss": int(sum(total_loss))})
        return Response(
            json.loads(dados_json), status=200, content_type="application/json"
        )


def find_index(list: list, value: str):
    try:
        return list.index(value)
    except ValueError:
        return None  # Retorna o indice 2 sendo o indice de empate


class Data(Dataset):
    def __init__(self) -> None:
        super().__init__()
        self.x = []
        self.y = []
        for match in Match.objects.all():
            game_line = [match.home_team.id, match.away_team.id]
            winner = find_index(game_line, match.winner.id) if match.winner else 2
            self.y.append(winner)
            self.x.append(torch.tensor(game_line, dtype=torch.float32))
        self.len = len(self.x)

    def __getitem__(self, index) -> tuple:
        return self.x[index], self.y[index]

    def __len__(self):
        return self.len
