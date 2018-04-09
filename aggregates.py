import pandas as pd
import numpy as np
from my_sql import get_connect

def create_df_query(table):
	aggregate_query = """
	SELECT * from {}
	""".format(table)
	return aggregate_query

def get_dataframe(table):
	conn = get_connect()
	df_query = create_df_query(table)
	df = pd.read_sql(df_query, conn)
	return df


def birth_range(x):
	year_gap = 1
	return ((ch.born_end >= x.born_start - year_gap) & (x.born_end + year_gap >= ch.born_start)).sum()


character_df = get_dataframe('CHARACTERS')
character_df.rename(columns={'id':'character_id'}, inplace=True)
house_df = get_dataframe('HOUSES')
house_df.rename(columns={'id':'house_id'}, inplace=True)
alliances_df = get_dataframe('HOUSE_FACT')

characters_and_alliances = pd.merge(character_df, alliances_df, on='character_id')
ch = pd.merge(characters_and_alliances, house_df, on='house_id')
ch['intersecting_birthyears'] = ch.apply(birth_range, axis=1)

print ch.head()
