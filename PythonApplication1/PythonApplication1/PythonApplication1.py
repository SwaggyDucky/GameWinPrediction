from asyncio.windows_events import NULL
import requests
import json
import tkinter as tk
from tkinter import ttk
from pprint import pprint
from typing import List
from player import RegisteredPlayer, register_player

def getInfo(call):
    r = requests.get(call)
    return r.json()

name = "pooradam"
API_KEY = "6"
name_link = f"https://api.hypixel.net/player?key={API_KEY}&name={name}"
data = getInfo(name_link)
file_path = 'C:\\Users\\averym\\AppData\\Roaming\\.minecraft\\logs\\latest.log'

with open(file_path, 'r') as f:
    lines = f.readlines()

for line in reversed(lines):
    if '[CHAT] ONLINE:' in line:
        names_string = line.split("[CHAT] ONLINE:")[1].strip()
        names = [name.strip() for name in names_string.split(",")]
        break

players: List[RegisteredPlayer] = []

for enemy in names:
    enemy_link = f"https://api.hypixel.net/player?key={API_KEY}&name={enemy}"
    enemy_data = getInfo(enemy_link)
    players.append(register_player(enemy_data, enemy))

root = tk.Tk()
root.title("Bedwars Stats")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(root, text="Name", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10)
ttk.Label(root, text="Total Wins", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=10, pady=10)
ttk.Label(root, text="Total Final Kills", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=10, pady=10)


for i, player in enumerate(players):
    ttk.Label(root, text=player.username).grid(row=i+1, column=0, padx=10, pady=5)
    ttk.Label(root, text=player.stats.wins).grid(row=i+1, column=1, padx=10, pady=5)
    ttk.Label(root, text=player.stats.fkills).grid(row=i+1, column=2, padx=10, pady=5)

root.mainloop()
