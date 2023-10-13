from app.service import AI

from torch.utils.data import DataLoader, Dataset
import torch

TEAMS_LIST = (
    "Argentina",
    "Bolívia",
    "Brasil",
    "Chile",
    "Colômbia",
    "Equador",
    "Paraguai",
    "Peru",
    "Uruguai",
    "Venezuela",
)
EPOCHS = 200


def find_index(list: list, value: str):
    try:
        return list.index(value)
    except ValueError:
        return 2  # Retorna o indice 2 sendo o indice de empate


class Data(Dataset):
    def __init__(self) -> None:
        super().__init__()
        self.x = []
        self.y = []
        with open("app/data/teams.txt", encoding="UTF-8") as file:
            for line in file.readlines():
                line = line.replace("\n", "").replace("\t", "")
                item = line.split("-")
                game_line = [find_index(TEAMS_LIST, team) for team in item[0:2]]
                winner = find_index(game_line, find_index(TEAMS_LIST, item[-1]))
                self.y.append(winner)
                self.x.append(game_line)
        self.len = len(self.x)

    def __getitem__(self, index) -> tuple:
        return self.x[index], self.y[index]

    def __len__(self):
        return self.len


def load_data() -> DataLoader:
    data_set = Data()
    data_loader = DataLoader(dataset=data_set, batch_size=2)
    return data_loader


def test_train_ai() -> None:
    data_loader = load_data()
    ai = AI()
    total_loss = ai.train(epochs=EPOCHS, data_loader=data_loader)
    ai.save()
    assert len(total_loss) != 0


def test_evaluate_ai() -> None:
    ai = AI()
    ai.load()
    home_team = "Uruguai"
    away_team = "Colômbia"
    winner = "Empate"
    game = [find_index(TEAMS_LIST, home_team), find_index(TEAMS_LIST, away_team)]
    winner = find_index(game, find_index(TEAMS_LIST, winner))
    result = ai.evaluate(torch.tensor(game, dtype=torch.float32))
    assert len(result) == 3
