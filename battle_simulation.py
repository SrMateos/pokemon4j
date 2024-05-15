from utils import exec_query
from queries import *


def damage(A, P, D, B, E):
    """
    Daño = 0.33 * B * E * ((A * P * (21)) / (25 * D) + 2 )
    A = Cantidad de ataque o ataque especial del Pokémon. Si el ataque que utiliza el Pokémon es físico se toma la cantidad de ataque y si es especial se toma la cantidad de ataque especial.
    P = Poder del ataque, el potencial del ataque.
    D = Cantidad de defensa del Pokémon rival. Si el ataque que hemos utilizado es físico cogeremos la cantidad de defensa del Pokémon rival, si el ataque que hemos utilizado es especial, se coge la cantidad de defensa especial del Pokémon rival.
    B = Bonificación. Si el ataque es del mismo tipo que el Pokémon que lo lanza toma un valor de 1.5, si el ataque es de un tipo diferente al del Pokémon que lo lanza toma un valor de 1.
    E = Efectividad. Puede tomar los valores de 0, 1, 2 y 4.
    """
    return 0.33 * B * E * ((A * P * (21)) / (25 * D) + 2)


def effectiveness(move_type, types_pokemon, type_chart):
    """
    Get the effectiveness of the move against the pokemon
    """
    return type_chart[move_type][types_pokemon[0]] * (
        1 if types_pokemon[1] is None else type_chart[move_type][types_pokemon[1]]
    )


def bonification(move_type, types_pokemon):
    """
    Get the bonification of the move against the pokemon
    """
    return 1.5 if move_type in types_pokemon else 1.0


def get_pokemon_types(pokemon_list):
    """
    Get the types of the pokemons
    """
    types = []
    for pokemon in pokemon_list:
        records, summary, keys = exec_query(
            QUERY_POKEMON_TYPES, {"name": pokemon["name"]}
        )
        types.append(
            [
                records[0].data()["t"]["name"],
                None if len(records) == 1 else records[1].data()["t"]["name"],
            ]
        )
    return types


def get_pokemon_moves(pokemon_list):
    """
    Get the moves of the pokemons
    """

    moves = []
    for pokemon in pokemon_list:
        records, summary, keys = exec_query(
            QUERY_POKEMON_MOVE, {"name": pokemon["name"]}
        )
        moves.append(records[0].data()["m"])

    return moves


def get_moves_types(moves):
    """
    Get the types of the moves
    """

    moves_types = []
    for move in moves:
        records, summary, keys = exec_query(QUERY_MOVE_TYPE, {"name": move["name"]})
        moves_types.append(records[0].data()["t"]["name"])

    return moves_types


def get_types_chart(types_list):
    """
    Get the types chart
    """
    types_chart = {}
    for type1 in types_list:
        aux = {}
        for type2 in types_list:
            records, summary, keys = exec_query(
                QUERY_TYPES_EFFECTIVITY, {"type1": type1, "type2": type2}
            )
            if len(records) == 0:
                damage = 1.0
            else:
                damage = records[0].data()["damage"]
            aux[type2] = damage

        types_chart[type1] = aux

    return types_chart


def attack_defense_simulation(pokemon_list):
    """
    Get the types of the pokemons and the moves and simulate an attack and defense between them
    """

    # Get the types of the pokemons
    types = get_pokemon_types(pokemon_list)

    # Get the moves of the pokemons
    moves = get_pokemon_moves(pokemon_list)

    # Get moves types
    moves_types = get_moves_types(moves)

    # Get the types chart
    total_types = list(
        set([t for sublist in types for t in sublist if t is not None] + moves_types)
    )
    type_chart = get_types_chart(total_types)

    print(f"The pokemons fighting are: {pokemon_list[0]['name']} and {pokemon_list[1]['name']}")
    print(f"The types of the pokemons are: {types[0]} and {types[1]}")
    print(f"The moves used are: {moves[0]['name']} and {moves[1]['name']}")
    print(f"The types of the moves are: {moves_types[0]} and {moves_types[1]}")

    # Calculate damage for first pokemon
    if moves[0]["category"] == "Physical":
        damage1 = damage(
            pokemon_list[0]["atk"],
            moves[0]["basePower"],
            pokemon_list[1]["def"],
            bonification(moves_types[0], types[0]),
            effectiveness(moves_types[0], types[1], type_chart),
        )
    else:
        damage1 = damage(
            pokemon_list[0]["spa"],
            moves[0]["basePower"],
            pokemon_list[1]["spd"],
            bonification(moves_types[0], types[0]),
            effectiveness(moves_types[0], types[1], type_chart),
        )

    # Calculate damage for second pokemon
    if moves[1]["category"] == "Physical":
        damage2 = damage(
            pokemon_list[1]["atk"],
            moves[1]["basePower"],
            pokemon_list[0]["def"],
            bonification(moves_types[1], types[1]),
            effectiveness(moves_types[1], types[0], type_chart),
        )
    else:
        damage2 = damage(
            pokemon_list[1]["spa"],
            moves[1]["basePower"],
            pokemon_list[0]["spd"],
            bonification(moves_types[1], types[1]),
            effectiveness(moves_types[1], types[0], type_chart),
        )
    print(f"Damage per move of {pokemon_list[0]["name"]}: {damage1}")
    print(f"Damage per move of {pokemon_list[1]["name"]}: {damage2}")

    # Calculate turns to defeat the other pokemon
    if damage1 != 0:
        turns1 = round(pokemon_list[1]["hp"] / damage1) + 1
    else:
        print(f"Attacks of the pokemon {pokemon_list[0]['name']} do not affect the pokemon {pokemon_list[1]['name']}")
        turns1 = 1_000_000_000

    if damage2 != 0:    
        turns2 = round(pokemon_list[0]["hp"] / damage2) + 1
    else:
        print(f"Attacks of the pokemon {pokemon_list[1]['name']} do not affect the pokemon {pokemon_list[0]['name']}")
        turns2 = 1_000_000_000

    # Print the winner
    if turns1 < turns2:
        print(f"The winner is {pokemon_list[0]["name"]} using {moves[0]['name']} in {turns1} turns")
    elif turns1 > turns2:
        print(f"The winner is {pokemon_list[1]["name"]} using {moves[1]['name']} in {turns2} turns")
    else:
        if turns1 == 1_000_000_000 and turns2 == 1_000_000_000:
            print("It's a tie")
        elif pokemon_list[0]["spe"] > pokemon_list[1]["spe"]:
            print(f"The winner is {pokemon_list[0]["name"]} using {moves[0]['name']} in {turns1} turns")
        else:
            print(f"The winner is {pokemon_list[1]["name"]} using {moves[1]['name']} in {turns2} turns")        


if __name__ == "__main__":
    lista = []

    records, summary, keys = exec_query(QUERY_POKEMON_BY_NAME, {"name": "Charizard"})
    for record in records:
        lista.append(record.data()["p"])

    records, summary, keys = exec_query(QUERY_POKEMON_BY_NAME, {"name": "Blastoise"})
    for record in records:
        lista.append(record.data()["p"])

    print("lista: ", lista)

    attack_defense_simulation(lista)
