from torch import exp, nn
from torch.utils.data import DataLoader
from torch.optim import Optimizer, Adam
import torch


class AI:
    def __init__(
        self,
        module: nn.Module = None,
        optimizer: Optimizer = None,
        criterion=None,
    ) -> None:
        self.module = module
        self.optimizer = optimizer
        self.criterion = criterion
        hidden_layers = 50
        if not self.module:
            self.module = nn.Sequential(
                nn.Linear(in_features=2, out_features=hidden_layers),
                nn.Linear(in_features=hidden_layers, out_features=3),
                nn.Sigmoid(),
                nn.Softmax(),
            )
        if not self.optimizer:
            self.optimizer = Adam(self.module.parameters(), lr=0.001)
        if not self.criterion:
            self.criterion = nn.CrossEntropyLoss()

    def train(self, epochs: int, data_loader: DataLoader) -> list[float]:
        losses = []
        for _ in range(epochs):
            for data in data_loader:
                teams, target = data
                teams = torch.stack(teams).float() if isinstance(teams, list) else teams
                self.optimizer.zero_grad()
                result = self.module(teams)
                loss = self.criterion(result, target)
                losses.append(loss.item())
                loss.backward()
                self.optimizer.step()
        return losses

    def evaluate(self, data: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            result = self.module(data)
            result = result * 100
        return result

    def save(self, save_path: str = "app/data/torch/teams_ai.chkpt") -> None:
        torch.save(self.module.state_dict(), save_path)

    def load(self, save_path: str = "app/data/torch/teams_ai.chkpt") -> bool:
        load = False
        try:
            state_dict = torch.load(save_path)
            self.module.load_state_dict(state_dict)
            load = True
        except Exception as e:
            pass
        return load
