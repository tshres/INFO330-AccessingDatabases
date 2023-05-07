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

for pokemon_id in sys.argv[1:]:
    pokemon_name = curr.execute(
    "SELECT name FROM pokemon WHERE id=?", (pokemon_id,)).fetchone()
    name = pokemon_name[0]
    print("Analyzing " + str(pokemon_id))

    type1 = curr.execute(
        "SELECT type1 FROM pokemon_types_view WHERE name=?", (pokemon_name[0],)).fetchall()
    type2 = curr.execute(
        "SELECT type2 FROM pokemon_types_view WHERE name=?", (pokemon_name[0],)).fetchall()


    strengths = []
    weaknesses = []
    for t in types:
        against = curr.execute("SELECT against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM pokemon_types_battle_view WHERE type1name=? AND type2name=?", (type1[0][0], type2[0][0])).fetchone()
        if against > 1:
            strengths.append(t)
        elif against < 1:
            weaknesses.append(t)

    print(f"{name} ({type1}, {type2}):")
    print("Strong against:", strengths)
    print("Weak against:", weaknesses)
    print()

    team.append(name)

answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    team_name = input("Enter the team name: ")
    cur.execute("INSERT INTO teams(name, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6) VALUES (?, ?, ?, ?, ?, ?, ?)", (team_name,) + tuple(team))
    conn.commit()
    print("Saving " + team_name + " ...")
else:
    print("Bye for now!")
