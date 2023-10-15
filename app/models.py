from django.db import models
import torch


class Team(models.Model):
    id: int = models.IntegerField(auto_created=True, primary_key=True)
    name: str = models.CharField(max_length=25)


class Match(models.Model):
    home_team: Team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_team"
    )
    away_team: Team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_team"
    )
    winner: Team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="winner", null=True, blank=True
    )

    def to_tensor(self):
        return torch.tensor([self.home_team.id, self.away_team.id], dtype=torch.float32)
