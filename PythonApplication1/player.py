from typing import Mapping
from dataclasses import dataclass
from pprint import pprint


@dataclass(frozen=True)
class Stats:
    wins: int
    losses: int
    fkills: int
    fdeaths: int
    bedsbroke: int
    bedslost: int
    fkdr: float

@dataclass(frozen=True)
class RegisteredPlayer:
    username: str
    stats: Stats

def register_player(playerdata: Mapping[str, object], username: str) -> RegisteredPlayer:

    bw_stats = playerdata.get('player', {}).get('stats', {}).get('Bedwars', {})
    wins = bw_stats.get("wins_bedwars", 0)
    losses = bw_stats.get("losses_bedwars", 0)
    fkills = bw_stats.get("final_kills_bedwars", 0)
    fdeaths = bw_stats.get("final_deaths_bedwars", 0)
    bedsbroke = bw_stats.get("beds_broken_bedwars", 0)
    bedslost = bw_stats.get("beds_lost_bedwars", 0)
    fkdr = round(fkills / fdeaths, 2) if fdeaths != 0 else round(fkills, 2)  # Or use float('inf') if you prefer



    return RegisteredPlayer(
        username=username,
        stats=Stats(wins=wins, 
                    fkills=fkills,
                    losses=losses,
                    fdeaths=fdeaths,
                    bedsbroke=bedsbroke,
                    bedslost=bedslost,
                    fkdr=fkdr
                    )
    )