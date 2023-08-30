import sqlite3
from typing import List
from player import RegisteredPlayer, Stats
import tkinter as tk
from tkinter import ttk

import sqlite3

def create_database(db_name: str = "player_stats.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create a table for the player stats
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS player_stats (
        username TEXT PRIMARY KEY,
        wins INTEGER,
        losses INTEGER,
        fkills INTEGER,
        fdeaths INTEGER,
        bedsbroke INTEGER,
        bedslost INTEGER,
        fkdr REAL,
        game_id INTEGER

    )
    """)

    conn.commit()
    conn.close()

def store_player_data(players: List[RegisteredPlayer], db_name: str = "player_stats.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(game_id) FROM player_stats")
    max_game_id = cursor.fetchone()[0]
    if max_game_id is None:
        max_game_id = 0

    for player in players:
        cursor.execute("""
        INSERT OR REPLACE INTO player_stats (username, wins, losses, fkills, fdeaths, bedsbroke, bedslost, fkdr, game_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (player.username, player.stats.wins, player.stats.losses, player.stats.fkills, player.stats.fdeaths,
              player.stats.bedsbroke, player.stats.bedslost, player.stats.fkdr, max_game_id + 1))

    conn.commit()
    conn.close()

def retrieve_player_data(db_name: str = "player_stats.db") -> List[RegisteredPlayer]:
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player_stats")
    rows = cursor.fetchall()

    players = []
    for row in rows:
        username, wins, losses, fkills, fdeaths, bedsbroke, bedslost, fkdr, _ = row
        player = RegisteredPlayer(username=username, stats=Stats(wins, losses, fkills, fdeaths, bedsbroke, bedslost, fkdr))
        players.append(player)

    conn.close()
    return players


#This method is just for testing purposes and will not be used in production.
#This is used to ensure the database is working correctly
def display_database(db_name: str = "player_stats.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM player_stats")
    rows = cursor.fetchall()

    conn.close()

    root = tk.Tk()
    root.title("Player Database")

    tree = ttk.Treeview(root, columns=("Name", "Wins", "Losses", "Final Kills", "Final Deaths", "Beds Broken", "Beds Lost", "FKDR", "Game ID"), show="headings")
    tree.heading("Name", text="Name")
    tree.heading("Wins", text="Wins")
    tree.heading("Losses", text="Losses")
    tree.heading("Final Kills", text="Final Kills")
    tree.heading("Final Deaths", text="Final Deaths")
    tree.heading("Beds Broken", text="Beds Broken")
    tree.heading("Beds Lost", text="Beds Lost")
    tree.heading("FKDR", text="FKDR")
    tree.heading("Game ID", text="Game ID")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.column("Name", width=100)
    tree.column("Wins", width=50)
    tree.column("Losses", width=50)
    tree.column("Final Kills", width=90)
    tree.column("Final Deaths", width=100)
    tree.column("Beds Broken", width=100)
    tree.column("Beds Lost", width=100)
    tree.column("FKDR", width=50)
    tree.column("Game ID", width=70)

    for row in rows:
        tree.insert("", "end", values=row)

    root.mainloop()
