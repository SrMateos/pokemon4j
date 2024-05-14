import neo4j
import json
import json5
import random
from queries import *
from menus import *
from utils import exec_query
from queries import *
from dump_data import dump_data

queries_dictionary = {
    '1': QUERY_POKEMON_BY_NAME,
    '2': QUERY_POKEMON_BY_TYPE,
    '3': QUERY_POKEMON_BY_ABILITY,
    '4': QUERY_POKEMON_BY_MOVE,
    '5': QUERY_POKEMON_BY_HEIGHT
}


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
    
    dump_data()

    print(greeting_message)

    pokemon = []
    for i in range(2):
        
        print(generation_message)

        generation = input("Enter the generation number: ")

        # Check if the input is a valid number between 1 and 8
        while generation not in ['1', '2', '3', '4', '5', '6', '7', '8']:
            print("Invalid input. Please enter a number between 1 and 8.")
            generation = input("Enter the generation number: ")

        print("Great! Here is the list of Pokémon from generation " + generation + ".")

        # QUERY SEGUN GENERACION
        result = exec_query(QUERY_POKEMON_BY_GENERATION, {"generation": generation})

        print(filter_message)

        filter_option = input("Enter the filter number: ")

        # Check if the input is a valid number between 1 and 4
        while filter_option not in ['1', '2', '3', '4', '5']:
            print("Invalid input. Please enter a number between 1 and 5.")
            filter_option = input("Enter the filter number: ")

        query = queries_dictionary[filter_option]

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