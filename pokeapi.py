import requests
import json
import os

from pokemon import Pokemon

def get_pokemon_information(pokemon=None):
    # checks if cache file exists and whether it has data for pokemon
    cache = validate_cache(pokemon)

    # use cached values if exists
    if cache:
        pokemon_data =  get_data_cache(pokemon)
        return get_pokemon_object(pokemon_data['id'], pokemon_data['name'], pokemon_data['type'], pokemon_data['encounter_location']) 

    try: 
        pokemon_data = get_data_api(pokemon) 

        # requires another api call
        location_encounters = get_location(pokemon_data['location_area_encounters'])

        # strip object to needed values
        type = get_type(pokemon_data['types'])
    except AssertionError as error:
        error = str(error)
        print(error)
        # TODO refactor error handling, perhaps move exception hanler to another module
        # not the best practice here but does the job for now
        exit()


    pokemon = get_pokemon_object(pokemon_data['id'], pokemon_data['name'], type, location_encounters)
   
   # save to txt if data is coming from api
    with open('cache.txt', 'a') as c: 
       c.write(json.dumps(pokemon.__dict__))
       c.write(os.linesep)

    return pokemon


def get_location(location_encounter_api=None):
    kanto_encounters = []
    locations = requests.get(location_encounter_api)

    for location in locations.json():
        if 'kanto'.lower() in location['location_area']['name'].lower():
            kanto_encounters.append({'area': location['location_area']['name'], 'method(s)': list(set(details['method']['name'] for version in location['version_details'] for details in version['encounter_details']))})


    assert kanto_encounters, 'No encounter in kanto, try again next time'
    return kanto_encounters

def get_type(types=None):
    for type in types:
        return {'slot': type['slot'], 'type': type['type']['name']}



def get_data_api(pokemon=None):
    pokemon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')

    assert pokemon_data.status_code != 404, f'No pokemon was found with the name or id of {pokemon}, try again'

    assert pokemon_data.status_code != 500, 'Something went wrong, perhaps pokemons are hiding'

    return pokemon_data.json()


def validate_cache(pokemon=None):
    cache_file = os.path.isfile('cache.txt')

    if not cache_file:
        return False

    with open('cache.txt') as c:
        pokemons = [json.loads(line) for line in c]

    for p in pokemons:
        if (p['name'] or p['id']) == pokemon: 
            return True

    return False


def get_data_cache(pokemon=None):
    pokemon_object = {}
    with open('cache.txt') as c:
        pokemons = [json.loads(line) for line in c]

    for p in pokemons:
        if (p['id'] or p['name'] == pokemon):
            pokemon_object = p

    return pokemon_object




def get_pokemon_object(id=None, name=None, type=None, encounter_location=None) -> Pokemon:
    return Pokemon(id, name, type, encounter_location)



