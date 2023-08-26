from typing import Mapping
from dataclasses import dataclass
from pprint import pprint


@dataclass(frozen=True)
class Stats:
    wins: int
    fkills: int

@dataclass(frozen=True)
class RegisteredPlayer:
    username: str
    stats: Stats

def register_player(playerdata: Mapping[str, object], username: str) -> RegisteredPlayer:

    print(f"Data for {username}:")
    pprint(playerdata)
    bw_stats = playerdata.get('player', {}).get('stats', {}).get('Bedwars', {})
    wins = bw_stats.get("wins_bedwars", 0)
    fkills = bw_stats.get("final_kills_bedwars", 0)

    return RegisteredPlayer(
        username=username,
        stats=Stats(wins=wins, fkills=fkills)
    )