import neo4j
from neo4j import GraphDatabase
import json
import json5
import random
from queries import *

queries = {
            '1': QUERY_POKEMON_BY_NAME,
            '2': QUERY_POKEMON_BY_TYPE,
            '3': QUERY_POKEMON_BY_ABILITY,
            '4': QUERY_POKEMON_BY_MOVE,
            '5': QUERY_POKEMON_BY_HEIGHT
}

def exec_query(query: str, params: dict):
    
    uri = "neo4j://localhost:7687"
    username = "neo4j"
    password = "password"
    database = "neo4j"
    
    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        records, summary, keys = driver.execute_query(query, params, database=database)
        return records, summary, keys

# Función para solicitar la entrada del usuario dependiendo del filtro elegido
def get_user_input_for_filter(filter_option):
    if filter_option == '1':
        return input("Enter the Pokémon name: ")
    elif filter_option == '2':
        return input("Enter the Pokémon type: ")
    elif filter_option == '3':
        return input("Enter the Pokémon ability: ")
    elif filter_option == '4':
        return input("Enter the Pokémon move: ")
    elif filter_option == '5':
        min_height = float(input("Enter the minimum height: "))
        max_height = float(input("Enter the maximum height: "))
        return min_height, max_height
    else:
        return None  # En caso de que se proporcione un filtro no válido


def main():
    greeting_message = """
        Welcome to Poke4J!

        Poke4J is your Pokémon comparator based on Neo4J. Get ready to discover everything about your favorite Pokémon!

        You can compare Pokémon based on different statistics to refine your search. You can filter by stats such as HP, Attack, Defense, Special Attack, Special Defense, and Speed.

        To get started, simply choose two Pokémon you'd like to compare and select the stats you want to consider for the comparison. We'll show you the differences between the Pokémon in those stats and any other relevant information.

        Have fun exploring the world of Pokémon with Poke4J!
    """

    print(greeting_message)

    pokemon = []
    for i in range(2):
        generation_message = """Please indicate the generation you want to play with:
            1. First generation.
            2. Second generation.
            3. Third generation.
            4. Fourth generation.
            5. Fifth generation.
            6. Sixth generation.
            7. Seventh generation.
            8. Eighth generation.
        """
        print(generation_message)

        generation = input("Enter the generation number: ")

        # Check if the input is a valid number between 1 and 8
        while generation not in ['1', '2', '3', '4', '5', '6', '7', '8']:
            print("Invalid input. Please enter a number between 1 and 8.")
            generation = input("Enter the generation number: ")

        print("Great! Here is the list of Pokémon from generation " + generation + ".")

        # QUERY SEGUN GENERACION
        result = exec_query(QUERY_POKEMON_BY_GENERATION, {"generation": generation})

        filter_message = """Please indicate the filter you want to use:
            1. Name
            2. Type
            3. Ability
            4. Move
            5. Height
            """

        print(filter_message)

        filter_option = input("Enter the filter number: ")

        # Check if the input is a valid number between 1 and 4
        while filter_option not in ['1', '2', '3', '4', '5']:
            print("Invalid input. Please enter a number between 1 and 5.")
            filter_option = input("Enter the filter number: ")

        query = queries[filter_option]

        user_input = get_user_input_for_filter(filter_option)

        if filter_option == '5':
            result = exec_query(query, {"min_height": user_input[0], "max_height": user_input[1]})
        else:
            result = exec_query(query, {"input": user_input})

        # MOSTRAR LISTA DE POKEMON
        print(result)

        print("Please, choose a Pokemon from the list:")

        pokemon = input()

        pokemon_list.push(pokemon)


if __name__ == '__main__':
    main()