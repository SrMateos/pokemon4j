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
    '3': QUERY_POKEMON_BY_WEIGHT,
    '4': QUERY_POKEMON_BY_GENERATION
}


def show_type_list():
    records, summary, keys = exec_query(QUERY_ALL_TYPES, {})
    for record in records:
        print(record['t']['name'])


def show_ability_list():
    records, summary, keys = exec_query(QUERY_ALL_ABILITIES_ASOCIATED_TO_POKEMONS, {})
    for record in records:
        print(record['a']['name'])


def show_generation_list(generation):
    records, summary, keys = exec_query(QUERY_POKEMON_BY_GENERATION, {"generation": generation})
    for record in records:
        print(record['g']['generation'])


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
    elif filter_option == '4':
        for i in range(1, 10):
            print(f"Generation {i}")
        return {"gen": int(input("Enter the generation number: "))}
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


def compare_habilities(pokemon_list):
    print()
    print("Comparing abilities")
    
    for pokemon in pokemon_list:
        record, summary, keys = exec_query(QUERY_ABILITY_BY_POKEMON, {"name": pokemon["name"]})
        print(f'{pokemon["name"]} has the ability {record[0].data()["a"]["name"]}')
        print(f'Description: {record[0].data()["a"]["description"]}')
        print()

def choose_pokemon():
    pokemon_number = 0
    
    apply_filter = input("Do you want to apply a filter to the list of Pokemon? (y/n)")
    records = []
    while apply_filter not in ['y', 'n']:
        print("Invalid input. Please enter 'y' or 'n'.")
        apply_filter = input("Do you want to apply a filter to the list of Pokemon? (y/n)")

    if apply_filter == 'n':
        records, summary, keys = exec_query(QUERY_ALL_POKEMON, {})
    
    else: 
        print(filter_message)

        filter_option = input("Enter the filter number: ")

        # Check if the input is a valid number between 1 and 4
        while filter_option not in ['1', '2', '3', '4']:
            print("Invalid input. Please enter a number between 1 and 3.")
            filter_option = input("Enter the filter number: ")

        query = queries_dictionary[filter_option]
        user_input = get_user_input_for_filter(filter_option)
        
        records, summary, keys = exec_query(query, user_input)

    # mientras que pokemon number no sea un número válido se seguirá pidiendo al usuario que introduzca un número
    for record in records:
        print(f'{record['p']['num']}.- {record['p']['name']}')
    print("Please, choose a Pokemon from the list (write the pokemon number):")

    pokemon_number = input()
    
    return pokemon_number


def compare_pokemon():
    pokemon_list_number = []
    for i in range(2):
        pokemon = choose_pokemon()
        pokemon_list_number.append(pokemon)
        
    pokemon_list = []

    print("You have chosen the following Pokemon:")

    for pokemon in pokemon_list_number:
        record, summary, keys = exec_query(QUERY_POKEMON_BY_NUMBER, {"num": int(pokemon)})
        pokemon_list.append(record[0].data()["p"])

    # bucle para seleccionar los distintos métodos de comparación
    method = -1
    while method != '0':
        print("Choose a method to compare the pokemons:")
        print("0.- Exit")
        print("1.- Compare stats")
        print("2.- Attack and defense simulation")
        print("3.- Compare abilities")

        method = input()
        
        if method == '1':
            compare_stats(pokemon_list)
            print()
            print()
        elif method == '2':
            attack_defense_simulation(pokemon_list)
            print()
            print()
        elif method == '3':
            compare_habilities(pokemon_list)
            print()
            print()
        elif method == '0':
            return
        else:
            print("Invalid method")

def create_movement():
    move_name   = input("Please introduce the move's name:")
    accuracy    = input("Please introduce the move's accuracy:")
    base_power  = input("Please introduce the move's base power:")
    pp          = input("Please introduce the move's power points:")
    category    = input("Please introduce the move's category:")
    description = input("Please introduce the move's description:")

    exec_query(INSERT_MOVE, {"name": move_name,
                             "accuracy": accuracy,
                             "basePower": base_power,
                             "pp": pp,
                             "category": category,
                             "description": description
                             })
    
    print("The move has been succesfully added to the database.")

def delete_movement():
    records, summary, keys = exec_query(QUERY_ALL_MOVES, {})
    for record in records:
        print(f'{record['m']['name']}')
    
    move_name = input("Please, choose a move to be deleted from the database (write the name):")
    exec_query(DELETE_MOVE, {"name": move_name})
    print("The move has been suffesfully deleted from the database.")

def update_movement():
    print("This is the list of movements:")
    records, summary, keys = exec_query(QUERY_ALL_MOVES, {})
    for record in records:
        print(f'{record['m']['name']}')

    move_name = input("Please, choose a move to be updated from the database (write the name):")
    
    new_move_name   = input("Please introduce the new move's name:")
    accuracy        = input("Please introduce the new move's accuracy:")
    base_power      = input("Please introduce the new move's base power:")
    pp              = input("Please introduce the new move's power points:")
    category        = input("Please introduce the new move's category:")
    description     = input("Please introduce the new move's description:")

    
    records, summary, keys = exec_query(UPDATE_MOVEMENT, {"name": move_name,
                                 "new_name": new_move_name,
                                 "accuracy": accuracy,
                                 "basePower": base_power,
                                 "pp": pp,
                                 "category": category,
                                 "description": description
                            })
    print(records)
    print(f'New move name: {records[0].data()['m']['name']}')
    print("The move has been suffesfully updated in the database.")

def update_pokemon_move():
    # Choose Pokemon to be updated
    pokemon = choose_pokemon()
    records, summary, keys = exec_query(QUERY_POKEMON_MOVE_BY_NUM, {"num": pokemon})
    for record in records:
        print(f'This is the actual Pokemon move: {record['m']['name']}')
    
    # Choose movement 
    print("This is the list of movements:")
    records, summary, keys = exec_query(QUERY_ALL_MOVES, {})
    for record in records:
        print(f'{record['m']['name']}')

    # Obtain new movement values.
    move_name = input("Please, choose a move from the list:")

    records, summary, keys = exec_query(QUERY_MOVE_BY_NAME, {"name": move_name})

    # Obtain actual pokemon move
    new_move = records[0].data()['m']['name']

    records, summary, keys = exec_query(UPDATE_POKEMON_MOVE, {"num": int(pokemon), "newMove": new_move})

    records, summary, keys = exec_query(QUERY_POKEMON_MOVE_BY_NUM, {"num": int(pokemon)})
    for record in records:
        print(f'The pokemon {pokemon} has the move {record['m']['name']}')
              
    print("The Pokemon's move has been succesfully updated in the database.")

# Crear movimiento
# Borrar movimiento
# Modificar movimiento
# Modificar el movimiento asociado a un pokemon
def movement_builder():
    options = -1
    while options != '0':
        print("Choose an option of the Movement Builder:")
        print("0.- Exit")
        print("1.- Create movement.")
        print("2.- Delete movement.")
        print("3.- Update movement.")
        print("4.- Update Pokemon move.")

        option = input()
        
        if option == '1':
            create_movement()
        elif option == '2':
            delete_movement()
        elif option == '3':
            update_movement()
        elif option == '4':
            update_pokemon_move()
        elif option == '0':
            return
        else:
            print("Invalid option")

def main():
    dump = input("Do you want to dump the data?(y/n)")
    if dump == 'y': 
        clear_db()  
        dump_data()
    else:
        print("Data will not be dumped")
    print(greeting_message)

    # Menu to compare pokemons exit or change movement of the pokemons
    option = -1
    while option != '0':
        print("Choose an option:")
        print("0.- Exit")
        print("1.- Compare Pokemon")
        print("2.- Movement Builder")

        option = input()

        if option == '1':
            compare_pokemon()
        elif option == '2':
            movement_builder()
        elif option == '0':
            print("Goodbye!")
        else:
            print("Invalid option")
    

    
    

if __name__ == '__main__':
    main()