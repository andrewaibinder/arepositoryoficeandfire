import MySQLdb

from config import get_main_configurations, get_db_configurations
from log import log


def get_connect():
	credentials = get_db_configurations()
	host = credentials['host']
	db = credentials['database']
	user = credentials['user']
	passwd = credentials['password']
	conn = MySQLdb.connect(db=db, user=user, passwd=passwd, host=host)
	return conn


def correct_format(column):
	col_type = type(column)
	if col_type == list or column == None:
		return False
	if column == "" or str(column).upper() == "NULL":
		return False
	return True


def row_cleaner(row):
	clean_row = []
	for col in row:		
		if type(col) == unicode:
			col = col.replace('\'', '\\\'')
			col = col.encode('latin-1')
		if correct_format(col):
			clean_col = "'{}'".format(col)
		else:
			clean_col = "NULL"
		clean_row.append(clean_col)
	return clean_row


def data_cleaner(data):
	clean_data = [row_cleaner(row) for row in data]
	return clean_data


def bulk_formatter(data):
	clean_data = data_cleaner(data)
	formatted_rows = ['({})'.format(",".join([str(c) for c in row]))
	                for row in clean_data]
	return """,
	""".join(formatted_rows)


def create_update_query(id, start_range, end_range):
	update_query = """
	UPDATE {}
	SET born_start = {}, born_end = {}
	WHERE id = {}""".format(character_table, start_range, end_range, id)
	return update_query	


def create_pull_all_query():
	select_query = """
	SELECT id, born from {}
	""".format(configs['character'])
	return select_query


def get_columns(table):
	column_key = "{}_cols".format(table)
	column_list = configs[column_key]
	return ", ".join(column_list)


def create_insert_query(bulk_data, table):
	columns = get_columns(table)
	formatted_data = bulk_formatter(bulk_data)
	insert_query = """
	INSERT INTO {}
	({})
	VALUES
	{}
	""".format(configs[table], columns, formatted_data)
	return insert_query


def select_all_names_query():
	select_query = """
	SELECT c.id, c.name
	FROM {} c
	inner join {} f on f.character_id = c.id
	WHERE name is not null AND
	name != ''
	""".format(configs['CHARACTERS'], configs['FACT'])
	return select_query


def create_clear_query(table):
	table_location = configs[table]
	select_query = """
	TRUNCATE {}
	""".format(table_location)
	return select_query


def select_character_by_id(character_id):
	select_query = """
	SELECT c.name, c.gender, h.name, c.born_start, c.born_end
	FROM {} f
	JOIN {} c on (f.character_id = c.id)
	JOIN {} h on (f.house_id = h.id)	
	WHERE f.character_id = {}
	""".format(configs['FACT'], configs['CHARACTERS'], configs['HOUSES'],
		       character_id)
	return select_query


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
		log("Error: unable to read data(pull_all_raw_born function)")
		log(e)
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
		log("Error: unable to write data(update_birth_range function)")
		log(e)
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
		log("Error: unable to read data(find_all_names function)")
		log(e)
		conn.rollback()
	conn.close()
	return names


def find_name_info(character_id):
	conn = get_connect()
	cursor = conn.cursor()
	id_query = select_character_by_id(character_id)
	id_values = None
	try:
		log(id_query)
		cursor.execute(id_query)
		id_values = cursor.fetchone()
	except Exception as e:
		log("Error: unable to read data(find_name_info function)")
		log(e)
		conn.rollback()
	conn.close()
	return id_values


def clear_table(table):
	conn = get_connect()
	cursor = conn.cursor()
	clear_query = create_clear_query(table)
	try:
		cursor.execute(clear_query)
		conn.commit()
	except Exception as e:
		log("Error: unable to write data(insert_new_house function)")
		log(e)
		conn.rollback()
	conn.close()


def insert_table(data, table):
	conn = get_connect()
	cursor = conn.cursor()
	insert_query = create_insert_query(data, table)
	try:
		cursor.execute(insert_query)
		conn.commit()
	except Exception as e:
		log("Error: unable to write data(insert_new_house function)")
		log(e)
		conn.rollback()
	conn.close()


def populate_tables(api_data):
	table_keys = [configs['FACT'], configs['CHARACTERS'], configs['HOUSES']]
	for table in table_keys:
		clear_table(table)
		insert_table(api_data[table], table)


configs = get_main_configurations()
