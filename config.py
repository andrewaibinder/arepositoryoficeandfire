import ConfigParser as cf

def get_main_configurations():
	config = cf.ConfigParser()
	config.read("config.ini")

	configurations = dict()
	configurations['CHARACTERS']=config.get('Tables', 'character_table')
	configurations['HOUSES']=config.get('Tables', 'house_table')
	configurations['FACT']=config.get('Tables', 'fact_table')

	configurations['CHARACTERS_cols']=config.get('Columns',
		                                        'character_columns').split()
	configurations['HOUSES_cols']=config.get('Columns',
									        'house_columns').split()
	configurations['FACT_cols']=config.get('Columns', 'fact_columns').split()

	configurations['domain']=config.get('API', 'domain')
	configurations['api_path']=config.get('API', 'api_path')
	configurations['book_path']=config.get('API', 'book_path')
	configurations['character_path']=config.get('API', 'character_path')
	configurations['house_path']=config.get('API', 'house_path')

	configurations['log_name']=config.get('Logs', 'log_name')
	configurations['log_directory']=config.get('Logs', 'log_directory')

	configurations['rough_shift'] =config.get('Magic Numbers', 'rough_shift')

	configurations['IP'] =config.get('Server', 'IP')
	configurations['Port'] =int(config.get('Server', 'Port'))
	configurations['Public'] =config.get('Server', 'Public')

	configurations['character_limit']=int(config.get('Debug',
		                                 'character_limit'))
	return configurations


def get_db_configurations():
	config = cf.ConfigParser()
	config.read("../credentials.ini")

	configs = dict()
	configs['host'] = config.get('User Credentials', 'host')
	configs['database'] = config.get('User Credentials', 'db')
	configs['user'] = config.get('User Credentials', 'user')
	configs['password'] = config.get('User Credentials', 'passwd')
	return configs

from config import get_main_configurations
