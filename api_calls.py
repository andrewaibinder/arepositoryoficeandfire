import requests
from my_sql import insert_new_character, insert_new_house, insert_house_member
from stat_calc import add_born_range

houses = dict()


def pull_id_from_url(url):
	if url == '':
		return None
	url_id = int(url.split('/')[-1])
	return url_id


def get_all_character_ids():
	print "Getting IDs"
	character_set = set()
	books_url = "https://www.anapioficeandfire.com/api/books"
	books_json = requests.get(books_url).json()
	for book in books_json:
		character_set.update([pull_id_from_url(url) for url in book['characters']])
		character_set.update([pull_id_from_url(url) for url in book['povCharacters']])
	return character_set


def get_character_info_by_id(character_id):
	global houses

	character_url = "https://anapioficeandfire.com/api/characters/{}".format(character_id) 	
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


def get_house_info_by_id(house):
	house_id = house['id']
	members = house['members']
	house_url = "https://anapioficeandfire.com/api/houses/{}".format(house_id)
	house = requests.get(house_url).json()
	house['id'] = house_id
	house['members'] = members
	house['currentLord'] = pull_id_from_url(house['currentLord'])
	house['founder'] = pull_id_from_url(house['founder'])
	house['swornMembers'] = [pull_id_from_url(member_url) for member_url in house['swornMembers']]
	house['members'].add(house['currentLord'])
	house['members'].add(house['founder'])
	house['members'].update(house['swornMembers'])

	return house

def populate_character_table(character_ids):
	for char_id in character_ids:
		character = get_character_info_by_id(char_id)
		character = add_born_range(character)
		insert_new_character(character)


def populate_house_table():
	for house_id in houses.keys():
		house = get_house_info_by_id(houses[house_id])
		insert_new_house(house)
		populate_house_fact_table(house['id'], house['members'])


def populate_house_fact_table(house_id, members):
	for member in members:
		if member != None:
			insert_house_member(house_id, member)


def populate_tables(character_ids):
	populate_character_table(character_ids)
	populate_house_table()


def start_process():
	character_ids = get_all_character_ids()
	populate_tables(character_ids)