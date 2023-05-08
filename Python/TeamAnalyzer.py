import sqlite3
import sys

conn = sqlite3.connect('../pokemon.sqlite')
curr = conn.cursor()

types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue

    pokemon_id_or_name = arg.strip().lower()
    if pokemon_id_or_name.isdigit():
        # Assume it's a Pokedex number
        pokemon_id = int(pokemon_id_or_name)
        pokemon_name = curr.execute(
            "SELECT name FROM pokemon WHERE id=?", (pokemon_id,)).fetchone()[0]
    else:
        # Assume it's a Pokemon name
        pokemon_name = pokemon_id_or_name.title()
        pokemon_id = curr.execute(
            "SELECT id FROM pokemon WHERE name=?", (pokemon_name,)).fetchone()[0]

    print("Analyzing " + str(pokemon_id) + " (" + pokemon_name + ")")

    type1 = curr.execute(
        "SELECT type1 FROM pokemon_types_view WHERE name=?", (pokemon_name,)).fetchone()[0]
    type2 = curr.execute(
        "SELECT type2 FROM pokemon_types_view WHERE name=?", (pokemon_name,)).fetchone()[0]

    for t in types:
        strengths = []
        weaknesses = []
        against = curr.execute("SELECT against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM pokemon_types_battle_view WHERE type1name=? AND type2name=?", (type1, type2)).fetchone()

        for k, val in enumerate(against):
            if val > 1:
                strengths.append(types[k])
            elif val < 1:
                weaknesses.append(types[k])

        print(pokemon_name + " (" + type1 + (" " + type2 if type2 else "") + ") is strong against", strengths, "but weak against", weaknesses)

    team.append(pokemon_name)

save_team = input("Would you like to save this team? (Y)es or (N)o: ")
if save_team.lower() == 'y':
    team_name = input("Enter the team name: ")
    curr.execute("INSERT INTO teams (name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6) VALUES (?, ?, ?, ?, ?, ?, ?)", (team_name,) + tuple(team))
    conn.commit()
    print("Saving Team " + team_name + " ...")
else:
    print("Bye for now!")