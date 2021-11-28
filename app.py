import json
import os.path

from pokeapi import get_pokemon_information

def start():
    print('Welcome traveler!')
    print('I will assist you in providing information for pokemons that could be encountered in Kanto region!')

    pokemon_input = input('Please let me know which pokemon are you looking for: ' )
    assert pokemon_input, 'I need to hear from to be able to help!'

    return pokemon_input


def fetch_pokemon():
    try:
        pokemon_input = start()
        pokemon = get_pokemon_information(pokemon_input.lower())
        print(json.dumps(pokemon.__dict__, sort_keys=False, indent=4))
    except AssertionError as error:
        error = str(error)
        if error == 'I need to hear from to be able to help, comeback when you are ready to talk!':
            print(error)

fetch_pokemon()
