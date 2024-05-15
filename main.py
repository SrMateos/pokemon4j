import neo4j
import json
import json5
import random
from queries import *
from menus import *
from utils import exec_query
from queries import *
from dump_data import dump_data, clear_db
import matplotlib.pyplot as plt
from battle_simulation import attack_defense_simulation

queries_dictionary = {
    '1': QUERY_POKEMON_BY_TYPE,
    '2': QUERY_POKEMON_BY_ABILITY,
    '3': QUERY_POKEMON_BY_WEIGHT
}


def show_type_list():
    records, summary, keys = exec_query(QUERY_ALL_TYPES, {})
    for record in records:
        print(record['t']['name'])


def show_ability_list():
    records, summary, keys = exec_query(QUERY_ALL_ABILITIES_ASOCIATED_TO_POKEMONS, {})
    for record in records:
        print(record['a']['name'])


def get_user_input_for_filter(filter_option):
    if filter_option == '1':
        show_type_list()
        return {"type": input("Enter the Pokémon type (write name): ")}
    
    elif filter_option == '2':  
        show_ability_list()
        return {"ability": input("Enter the Pokémon ability: ")}
    
    elif filter_option == '3':
        min_weight = float(input("Enter the minimum height: "))
        max_weight = float(input("Enter the maximum height: "))
        return {"min_weight": min_weight, "max_weight": max_weight}
    
    else:
        return None  


def compare_stats(pokemon_list):
    stats = ["hp", "atk", "def", "spa", "spd", "spe", "weightkg", "heightm"]
    color = ['Red', 'Green']
    fig, ax = plt.subplots()
    bar_width = 0.35
    x = range(len(stats))
    for i, pokemon in enumerate(pokemon_list):
        ax.bar([p + bar_width * i for p in x], [pokemon[stat] for stat in stats], bar_width, label=pokemon["name"], color=color[i])
    ax.set_xlabel('Stats')
    ax.set_ylabel('Values')
    ax.set_title('Pokemon stats comparison')
    ax.set_xticks([p + bar_width for p in x])
    ax.set_xticklabels(stats)
    ax.legend()
    plt.show()


def main():
    dump = input("Do you want to dump the data?(y/n)")
    if dump == 'y': 
        clear_db()  
        dump_data()
    else:
        print("Data will not be dumped")

    print(greeting_message)

    pokemon_list_number = []
    for i in range(2):

        apply_filter = input("Do you want to apply a filter to the list of Pokemon? (y/n)")
        while apply_filter not in ['y', 'n']:
            print("Invalid input. Please enter 'y' or 'n'.")
            apply_filter = input("Do you want to apply a filter to the list of Pokemon? (y/n)")

        if apply_filter == 'n':
            records, summary, keys = exec_query(QUERY_ALL_POKEMON, {})
            for record in records:
                print(f'{record['p']['num']}.- {record['p']['name']}')
        
        else: 
            print(filter_message)

            filter_option = input("Enter the filter number: ")

            # Check if the input is a valid number between 1 and 4
            while filter_option not in ['1', '2', '3']:
                print("Invalid input. Please enter a number between 1 and 3.")
                filter_option = input("Enter the filter number: ")

            query = queries_dictionary[filter_option]
            user_input = get_user_input_for_filter(filter_option)
             
            records, summary, keys = exec_query(query, user_input)

            # MOSTRAR LISTA DE POKEMON
            for record in records:
                print(f'{record['p']['num']}.- {record['p']['name']}')

        print("Please, choose a Pokemon from the list (write the pokemon number):")
        pokemon = input()
        pokemon_list_number.append(pokemon)
    
    pokemon_list = []
    print("You have chosen the following Pokemon:")
    for pokemon in pokemon_list_number:
        record, summary, keys = exec_query(QUERY_POKEMON_BY_NUMBER, {"num": int(pokemon)})
        print(record[0].data()["p"])
        pokemon_list.append(record[0].data()["p"])
    
    print("You have chosen the following Pokemon:")
    for pokemon in pokemon_list:
        print(pokemon["name"])

    # bucle para seleccionar los distintos métodos de comparación
    method = -1
    while method != 0:
        print("Choose a method to compare the pokemons:")
        print("0.- Exit")
        print("1.- Compare stats")
        print("2.- Attack and defense simulation")

        method = input()
        
        if method == '1':
            compare_stats(pokemon_list)
        elif method == '2':
            attack_defense_simulation(pokemon_list)
        elif method == '0':
            print("Goodbye!")
        else:
            print("Invalid method")
    

if __name__ == '__main__':
    main()