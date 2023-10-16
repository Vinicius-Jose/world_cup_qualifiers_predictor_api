from app.models import Match, Team

TEAMS_LIST = (
    "Argentina",
    "Bolivia",
    "Brasil",
    "Chile",
    "Colombia",
    "Equador",
    "Paraguai",
    "Peru",
    "Uruguai",
    "Venezuela",
)


def load_data():
    Match.objects.all().delete()
    Team.objects.all().delete()
    with open("app/data/teams.txt", encoding="UTF-8") as file:
        for line in file.readlines():
            line = line.replace("\n", "").replace("\t", "")
            item = line.split("-")
            home_team, created = Team.objects.update_or_create(
                id=find_index(TEAMS_LIST, item[0]) + 1, name=item[0]
            )
            away_team, created = Team.objects.update_or_create(
                id=find_index(TEAMS_LIST, item[1]) + 1, name=item[1]
            )
            game_id = [home_team.id, away_team.id]
            game = [home_team, away_team]
            winner_index = find_index(TEAMS_LIST, item[-1])
            winner_index = (
                find_index(game_id, winner_index + 1)
                if winner_index is not None
                else winner_index
            )
            winner = game[winner_index] if winner_index is not None else winner_index

            match = Match.objects.create(
                home_team=home_team, away_team=away_team, winner=winner
            )


load_data()


def find_index(list: list, value: str):
    try:
        return list.index(value)
    except ValueError:
        return None  # Retorna o indice 2 sendo o indice de empate
