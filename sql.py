import MySQLdb
import pandas as pd

from config import get_main_configurations, get_db_configurations
from log import log
from sqlalchemy import create_engine


def get_connect():
	credentials = get_db_configurations()
	host = credentials['host']
	db = credentials['database']
	user = credentials['user']
	passwd = credentials['password']
	conn = MySQLdb.connect(db=db, user=user, passwd=passwd, host=host)
	return conn


def get_engine_connect():
	credentials = get_db_configurations()
	host = credentials['host']
	db = credentials['database']
	user = credentials['user']
	passwd = credentials['password']
	engine = create_engine("mysql://{}:{}@{}/{}".format(user, passwd, host, db))
	conn = engine.connect()
	return conn


def select_all_names_query():
	select_query = """
	SELECT c.id, c.name
	FROM {} c
	inner join {} f on f.character_id = c.id
	WHERE name is not null
	""".format(configs['CHARACTERS'], configs['FACT'])
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


def get_columns(table):
	column_key = "{}_cols".format(table)
	column_list = configs[column_key]
	return column_list


def build_table(data, table):
	engine_conn = get_engine_connect()
	labels = get_columns(table)
	df = pd.DataFrame(data, columns=labels)
	df.to_sql(table, engine_conn, flavor=None, schema=None,
          if_exists='replace', index=True, index_label=None,
          chunksize=None, dtype=None)


def populate_tables(api_data):
	table_keys = [configs['FACT'], configs['CHARACTERS'], configs['HOUSES']]
	for table in table_keys:
		build_table(api_data[table], table)


def create_df_query(table):
    aggregate_query = """
    SELECT * from {}
    """.format(table)
    return aggregate_query


def get_dataframe(table):
    engine_conn = get_engine_connect()
    df_query = create_df_query(table)
    df = pd.read_sql(df_query, engine_conn)
    return df


def get_name_dataframe():
    engine_conn = get_engine_connect()
    df_query = select_all_names_query()
    df = pd.read_sql(df_query, engine_conn)
    return df


def get_lookup_dataframe(character_id):
    engine_conn = get_engine_connect()
    df_query = select_character_by_id(character_id)
    df = pd.read_sql(df_query, engine_conn)
    return df


def find_name_info(character_id):
	lookup_df = get_lookup_dataframe(character_id)
	character_data = lookup_df.values.tolist()
	houses = []
	for row in character_data:
		houses.append(row[2])
	character_list = character_data[0]
	character_list[2] = houses
	return character_list


def find_all_names():
	name_list_df = get_name_dataframe()
	return name_list_df.values.tolist()


configs = get_main_configurations()
