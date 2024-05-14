import neo4j
from neo4j import GraphDatabase
import json
import json5
import random
from queries import *
from utils import exec_query

def createPokemon(pokemon):
    return {
        "name": pokemon["name"],
        "num": pokemon["num"],
        "gen": pokemon["gen"],
        "heightm": pokemon["heightm"],
        "weightkg": pokemon["weightkg"],
        "hp": pokemon["baseStats"]["hp"],
        "atk": pokemon["baseStats"]["atk"],
        "def": pokemon["baseStats"]["def"],
        "spa": pokemon["baseStats"]["spa"],
        "spd": pokemon["baseStats"]["spd"],
        "spe": pokemon["baseStats"]["spe"]
    } 

def createMove(move):
    return {
        "name": move["name"],
        "accuracy": move["accuracy"],
        "basePower": move["basePower"],
        "pp": move["pp"],
        "category": move["category"],
        "description": move["shortDesc"]
    }

def dump_types_chart():
    types_chart = {
        "Normal": {"Ghost": 0.0},
        "Fighting": {"Normal": 2.0, "Rock": 2.0, "Ghost": 0.0, "Steel": 2.0, "Ice": 2.0, "Dark": 2.0},
        "Flying": {"Fighting": 2.0, "Bug":2.0, "Grass": 2.0},
        "Poison": {"Steel": 0.0, "Grass": 2.0, "Fairy": 2.0},
        "Ground": {"Flying": 0.0, "Poison": 2.0, "Rock": 2.0, "Steel": 2.0, "Fire": 2.0, "Electric": 0.0},
        "Rock": {"Flying": 2.0, "Bug": 2.0, "Fire": 2.0, "Ice": 2.0},
        "Bug": {"Grass": 2.0, "Psychic": 2.0, "Dark": 2.0},
        "Ghost": {"Normal": 0.0, "Ghost": 2.0, "Psychic": 2.0},
        "Steel": {"Rock": 2.0, "Ice": 2.0, "Fairy": 2.0},
        "Fire": {"Bug": 2.0, "Steel": 2.0, "Grass": 2.0, "Ice": 2.0},
        "Water": {"Ground": 2.0, "Rock": 2.0, "Fire": 2.0},
        "Grass": {"Ground": 2.0, "Rock": 2.0, "Water": 2.0},
        "Electric": {"Flying": 2.0, "Ground": 0.0, "Water": 2.0},
        "Psychic": {"Fighting": 2.0, "Poison": 2.0, "Dark": 0.0},
        "Ice": {"Flying": 2.0, "Ground": 2.0, "Grass": 2.0, "Dragon": 2.0},
        "Dragon": {"Dragon": 2.0, "Fairy": 0.0},
        "Dark": {"Ghost": 2.0, "Psychic": 2.0},
        "Fairy": {"Fighting": 2.0, "Dragon": 2.0, "Dark": 2.0}
    }

    for type1 in types_chart:
        for type2 in types_chart[type1]:
            exec_query(INSERT_TYPE_CHART, {"type1": type1, "type2": type2, "damage": types_chart[type1][type2]})                      


def dump_data():
    # Dump abilities
    with open('abilities.json5') as abilities:
        abilities_data = json5.load(abilities)
        for ability in abilities_data:
            exec_query(INSERT_ABILITY, {"name": ability, "description": abilities_data[ability]["shortDesc"]})

    with open('pokedex.json') as pokedex:
        with open('learnsets.json') as learnset:
            with open('moves.json') as moves:    
                pokedex_data = json.load(pokedex)
                learnset_data = json.load(learnset)
                moves_data = json.load(moves)

                # Types 
                types =  set([type for pokemon in pokedex_data for type in pokedex_data[pokemon]["types"] if pokedex_data[pokemon]["num"] > 0])
                for type in types:
                    exec_query(INSERT_TYPE, {"name": type})

                # Pokemons
                for pokemon in pokedex_data:
                    if pokedex_data[pokemon]["num"] > 0 and "-" not in pokedex_data[pokemon]["name"]:
                        exec_query(INSERT_POKEMON, createPokemon(pokedex_data[pokemon]))

                        # Relation pokemon with types
                        for type in pokedex_data[pokemon]["types"]:
                            exec_query(INSERT_POKEMON_TYPE, {"pokemon": pokedex_data[pokemon]["name"], "type": type})

                        # Relation pokemon with abilities
                        for ability in pokedex_data[pokemon]["abilities"].values():
                            exec_query(INSERT_POKEMON_ABILITY, {"pokemon": pokedex_data[pokemon]["name"], "ability": ability.lower()})

                        # Take random move 
                        random_move = moves_data[random.choice(list(learnset_data[pokemon]["learnset"]))]

                        # Create move
                        exec_query(INSERT_MOVE, createMove(random_move))

                        # Relation pokemon with move
                        exec_query(INSERT_POKEMON_MOVES, {"pokemon": pokedex_data[pokemon]["name"], "move": random_move["name"]})

                        # Relation move with type
                        exec_query(INSERT_MOVES_TYPE, {"move": random_move["name"], "type": random_move["type"]}) 
    
    dump_types_chart()