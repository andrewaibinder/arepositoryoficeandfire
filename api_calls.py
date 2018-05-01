import requests
from stat_calc import add_born_range
from log import log
from config import get_main_configurations


def pull_id_from_url(url):
    if url == '':
        return None
    url_id = int(url.split('/')[-1])
    return url_id


def generate_base_url(choice_path):
    domain = configs['domain']
    api_path = configs['api_path']
    return "https://{}/{}/{}/".format(domain, api_path, choice_path)


def get_all_character_ids():
    log("Getting IDs")
    character_set = set()
    books_url = generate_base_url(configs['book_path'])
    books_json = requests.get(books_url).json()
    for book in books_json:
        character_set.update([pull_id_from_url(url) for url in
                             book['characters']])
        character_set.update([pull_id_from_url(url) for url in
                             book['povCharacters']])
    return character_set


def get_character_info_by_id(character_id):
    global houses

    base_url = generate_base_url(configs['character_path'])
    character_url = "{}{}".format(base_url, character_id)
    try:
        character = requests.get(character_url).json()
        character['id'] = character_id
        for house_url in character['allegiances']:
            house_id = pull_id_from_url(house_url)
            if house_id not in houses.keys():
                houses[house_id] = dict()
                houses[house_id]['id'] = house_id
                houses[house_id]['members'] = set()
            houses[house_id]['members'].add(character_id)
        return character
    except:
        log("Error with: {}".format(character_url))
        return None
    

def get_house_info_by_id(house):
    house_id = house['id']
    members = house['members']
    base_url = generate_base_url(configs['house_path'])
    house_url = "{}{}".format(base_url, house_id)
    house = requests.get(house_url).json()
    house['id'] = house_id
    house['members'] = members
    house['currentLord'] = pull_id_from_url(house['currentLord'])
    house['founder'] = pull_id_from_url(house['founder'])
    house['swornMembers'] = [pull_id_from_url(member_url) for member_url in
                             house['swornMembers']]
    house['members'].add(house['currentLord'])
    house['members'].add(house['founder'])
    house['members'].update(house['swornMembers'])
    return house


def gather_character_data():
    character_ids = get_all_character_ids()
    data_dict = {}
    character_data = []
    for char_id in character_ids:
        if char_id > configs['character_limit']:
            break
        character = get_character_info_by_id(char_id)
        if character is not None:
            character = add_born_range(character)
            character_data.append([character[column] for column in
                                  configs['CHARACTERS_cols']])
    data_dict[configs['CHARACTERS']] = character_data
    return data_dict


def gather_house_and_fact_data():
    data_dict = {}
    house_data = []
    fact_data = []
    for house_id in houses.keys():
        house = get_house_info_by_id(houses[house_id])
        house_data.append([house[column] for column
                         in configs['HOUSES_cols']])
        for member in house['members']:
            if member is not None:
                fact_data.append([house['id'], member])
    data_dict[configs['HOUSES']] = house_data
    data_dict[configs['FACT']] = fact_data
    return data_dict


def get_api_data():
    api_data = dict()
    api_data.update(gather_character_data())
    api_data.update(gather_house_and_fact_data())
    return api_data


configs = get_main_configurations()
houses = dict()
