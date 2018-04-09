import MySQLdb
import ConfigParser as cf

character_table = "CHARACTERS"
house_table = "HOUSES"
character_house_fact_table = "HOUSE_FACT"
character_full_table = "intersected_characters"

def get_connect():

	config = cf.ConfigParser()
	config.read("../credentials.ini")
	db=config.get('User Credentials', 'db')
	user=config.get('User Credentials', 'user')
	passwd=config.get('User Credentials', 'passwd')
	host=config.get('User Credentials', 'host')
	conn = MySQLdb.connect(db=db, user=user, passwd=passwd, host=host)
	return conn


def data_cleaner(entry):
	clean_data = {}
	for key in entry.keys():
		if type(entry[key]) != list and entry[key] != None and entry[key] != "":
			if type(entry[key]) == unicode:
				value = entry[key]
				value = value.replace('\'', '\\\'')
				value = value.encode('latin-1')
			else:
				value = entry[key]
			clean_data[key] = "'{}'".format(value)
		else:
			clean_data[key] = "NULL"
	return clean_data


def create_insert_character_query(character):
	character = data_cleaner(character)
	insert_query = """
	INSERT INTO {}
	(id, name, gender, culture, born, born_start, born_end, died, father, mother, spouse)
	VALUES
	({},{},{},{},{},{},{},{},{},{},{})
	""".format(character_table, character['id'], character['name'], character['gender'], character['culture'], character['born'], character['born_start'], character['born_end'], character['died'], character['father'], character['mother'], character['spouse'])
	return insert_query


def create_update_query(id, start_range, end_range):
	update_query = """
	UPDATE {}
	SET born_start = {}, born_end = {}
	WHERE id = {};""".format(character_table, start_range, end_range, id)
	return update_query	


def create_pull_all_query():
	select_query = """
	SELECT id, born from {}
	""".format(character_table)
	return select_query


def create_house_member_insert_query(house_id, character_id):
	insert_query = """
	INSERT INTO {}
	(house_id, character_id)
	VALUES
	({},{})
	""".format(character_house_fact_table, house_id, character_id)
	return insert_query


def create_house_insert_query(house):
	house = data_cleaner(house)
	insert_query = """
	INSERT INTO {}
	(id, name, region, coatOfArms, words, currentLord, heir, founder, diedOut)
	VALUES
	({},{},{},{},{},{},{},{},{})
	""".format(house_table, house['id'], house['name'], house['region'], house['coatOfArms'], house['words'], house['currentLord'], house['heir'], house['founder'], house['diedOut'])
	return insert_query


def select_all_names_query():
	select_query = """
	SELECT character_id, name_x FROM {}
	WHERE character_id is not null and name_x is not null
	""".format(character_full_table)
	return select_query


def select_character_by_id(character_id):
	select_query = """
	SELECT *
	FROM {}
	WHERE character_id = {}
	""".format(character_full_table, character_id)
	return select_query


def insert_new_character(character_data):
	conn = get_connect()
	cursor = conn.cursor()
	insert_query = create_insert_character_query(character_data)
	try:
		cursor.execute(insert_query)
		conn.commit()
	except Exception as e:
		if "Duplicate entry" not in str(e):
			print "Error: unable to write data(insert_new_character function)"
			print (e)
		conn.rollback()
	conn.close()


def pull_all_raw_born():
	conn = get_connect()
	cursor = conn.cursor()
	characters = []
	select_query = create_pull_all_query()
	try:
		cursor.execute(select_query)
		results = cursor.fetchall()
		for row in results:
			character = dict()
			character['id'] = int(row[0])
			character['born'] = row[1]
			characters.append(character)
	except Exception as e:
		print "Error: unable to read data(pull_all_raw_born function)"
		print (e)
		conn.rollback()
	conn.close()
	return characters


def update_birth_range(id, start_range, end_range):
	conn = get_connect()
	cursor = conn.cursor()
	update_query = create_update_query(id, start_range, end_range)
	try:
		cursor.execute(update_query)
		conn.commit()
	except Exception as e:
		print "Error: unable to write data(update_birth_range function)"
		print (e)
		conn.rollback()
	conn.close()


def insert_house_member(house_id, character_id):
	conn = get_connect()
	cursor = conn.cursor()
	insert_query = create_house_member_insert_query(house_id, character_id)
	try:
		cursor.execute(insert_query)
		conn.commit()
	except Exception as e:
		print "Error: unable to write data(insert_house_member function)"
		print (e)
		conn.rollback()
	conn.close()


def insert_new_house(house):
	conn = get_connect()
	cursor = conn.cursor()
	insert_query = create_house_insert_query(house)
	try:
		cursor.execute(insert_query)
		conn.commit()
	except Exception as e:
		print "Error: unable to write data(insert_new_house function)"
		print (e)
		conn.rollback()
	conn.close()


def find_all_names():
	conn = get_connect()
	cursor = conn.cursor()
	select_query = select_all_names_query()
	names = []
	try:
		cursor.execute(select_query)
		results = cursor.fetchall()
		for row in results:
			character_id = row[0]
			character_name = row[1]
			if character_name == '':
				character_name = "Unknown Character"
			names.append([character_id, character_name])
	except Exception as e:
		print "Error: unable to read data(find_all_names function)"
		print (e)
		conn.rollback()
	conn.close()
	return names


def find_name_info(character_id):
	conn = get_connect()
	cursor = conn.cursor()
	id_query = select_character_by_id(character_id)
	print id_query
	id_values = None
	try:
	    cursor.execute(id_query)
	    id_values = cursor.fetchone()
	except Exception as e:
		print "Error: unable to read data(find_all_names function)"
		print (e)
		conn.rollback()
	conn.close()
	return id_values
