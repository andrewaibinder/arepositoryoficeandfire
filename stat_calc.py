import re
from my_sql import pull_all_raw_born, update_birth_range


def clean_numbers(raw_numbers):
	return [int(n) for n in raw_numbers]


def value_extractor(born_string, extract_style):

	if extract_style == 'only':
		numbers = re.findall(r'\b\d+\b', born_string)
		numbers = clean_numbers(numbers)
		return (numbers[0], numbers[0])

	if extract_style == 'only_roughly':
		numbers = re.findall(r'\b\d+\b', born_string)
		numbers = clean_numbers(numbers)
		return (numbers[0]-1, numbers[0]+1)

	if extract_style == 'only_negative':
		numbers = re.findall(r'\b\d+\b', born_string)
		numbers = clean_numbers(numbers)
		return (numbers[0] * -1, numbers[0] * -1)

	if extract_style == 'first_second':
		numbers = re.findall(r'\b\d+\b', born_string)
		numbers = clean_numbers(numbers)
		return (min(numbers), max(numbers))

	if extract_style == 'first_neg_second_neg':
		numbers = re.findall(r'\d+', born_string)
		numbers = clean_numbers(numbers)
		return (max(numbers) * -1, min(numbers) * -1)

	if extract_style == 'first_second_roughly':
		numbers = re.findall(r'\d+', born_string)
		numbers = clean_numbers(numbers)
		numbers.append((min(numbers) - 1))
		numbers.append((max(numbers) + 1))
		return (min(numbers), max(numbers))		

	if extract_style == 'in_or_after':
		numbers = re.findall(r'\d+', born_string)
		numbers = clean_numbers(numbers)
		return (min(numbers), "NULL")

	if extract_style == 'in_or_before':
		numbers = re.findall(r'\d+', born_string)
		numbers = clean_numbers(numbers)
		return ("NULL", max(numbers))

	if extract_style == 'in_or_before_roughly':
		numbers = re.findall(r'\d+', born_string)
		numbers = clean_numbers(numbers)
		return ("NULL", max(numbers) + 1)

	return ("NULL", "NULL")


def collect_templates():

	template_dict = dict()
	template_dict[r'\AIn \d{1,3} AC\Z'] = "only"
	template_dict[r'\AIn \d{1,3} AC, at '] = "only"
	template_dict[r'\AAt \d{1,3} AC\Z'] = "only"
	template_dict[r'\A\d{1,3} AC\Z'] = "only"
	template_dict[r'\A\d{1,3} AC, at '] = "only"

	template_dict[r'\AIn \d{1,3} AC \(roughly\)\Z'] = "only_roughly"
	template_dict[r'\AIn \d{1,3} AC \(roughly\), at'] = "only_roughly"
	template_dict[r'\AIn or around \d{1,3} AC\Z'] = "only_roughly"
	template_dict[r'\AIn about \d{1,3} AC, at'] = "only_roughly"
	template_dict[r'\AIn or around \d{1,3} AC \(roughly\)'] = "only_roughly"

	template_dict[r'\AIn or between \d{1,3} AC and \d{1,3} AC\Z'] = 'first_second'
	template_dict[r'\AIn or between \d{1,3} AC and \d{1,3} AC, at'] = 'first_second'
 	template_dict[r'\AIn \d{1,3} AC or \d{1,3} AC\Z'] = 'first_second'
 	template_dict[r'\AIn \d{1,3} AC or \d{1,3} AC, at'] = 'first_second'
	template_dict[r'\AIn or between \d{1,3} AC or \d{1,3} AC\Z'] = 'first_second'
	template_dict[r'\AIn \d{1,3} or \d{1,3} AC\Z'] = 'first_second'
	template_dict[r'\AIn either \d{1,3} AC, \d{1,3} AC or \d{1,3} AC\Z'] = 'first_second'
	template_dict[r'\AIn either \d{1,3} AC, \d{1,3} AC or \d{1,3} AC, at'] = 'first_second'
	template_dict[r'\AIn \d{1,3} AC, \d{1,3} AC or \d{1,3} AC\Z'] = 'first_second'
	template_dict[r'\AIn \d{1,3} AC, \d{1,3} AC or \d{1,3} AC, at'] = 'first_second'
	template_dict[r'\AIn or around \d{1,3} AC, \d{1,3} AC or \d{1,3} AC'] = 'first_second'
	template_dict[r'\AAt \d{1,3} AC or \d{1,3} AC\Z'] = 'first_second'
	template_dict[r'\AIn \d{1,3} AC and \d{1,3} AC\Z'] = 'first_second'
	template_dict[r'\Aor between \d{1,3} AC and \d{1,3} AC, at'] = 'first_second'
	template_dict[r'\AAt \d{1,3} AC, \d{1,3} AC or \d{1,3} AC\Z'] = 'first_second'

	template_dict[r'\AIn or between ~\d{1,3} AC and \d{1,3} AC\Z'] = "first_second_roughly"
	template_dict[r'\AIn or between ~\d{1,3} AC and \d{1,3} AC\Z'] = "first_second_roughly"
	template_dict[r'\AIn or between \d{1,3} AC and \d{1,3} AC \(roughly\)\Z'] = "first_second_roughly"
	template_dict[r'\AIn or between \d{1,3} AC and \d{1,3} AC \(roughly\), at'] = "first_second_roughly"

	template_dict[r'\AIn \d{1,3}AC or after\Z'] = "in_or_after"
	template_dict[r'\AIn \d{1,3} AC or later\Z'] = "in_or_after"
	template_dict[r'\AIn After \d{1,3} AC\Z'] = "in_or_after"
	template_dict[r'\AIn \d{1,3} AC or later, at'] = "in_or_after"

	template_dict[r'\AIn or before \d{1,3} AC\Z'] = "in_or_before"	
	template_dict[r'\Aor before \d{1,3} AC\Z'] = "in_or_before"
	template_dict[r'\AIn \d{1,3} AC or before\Z'] = "in_or_before"
	template_dict[r'\AIn \d{1,3} AC or before, at'] = "in_or_before"

	template_dict[r'\AIn \d{1,3} AC or before \(roughly\)\Z'] = "in_or_before_roughly"
	template_dict[r'\A\d{1,3} BC, at'] = "only_negative"
	template_dict[r'\AIn \d{1,3}BC or \d{1,3}BC, at'] = "first_neg_second_neg"

	return template_dict


def born_parser(born_string):
	templates = collect_templates()
	if born_string != None:
		for key in templates.keys():
			if re.match(key, born_string):
				return value_extractor(born_string, templates[key])
	return ("NULL","NULL")


def num_there(s):
    return any(i.isdigit() for i in s)


def add_born_range(character):
	birth_range = born_parser(character['born'])
	character['born_start'] = birth_range[0]
	character['born_end'] = birth_range[1]
	if character['born'] != None and num_there(character['born']) and birth_range == ("NULL","NULL"):
		print character['born']
	return character


def find_born_range_list_of_characters(characters):
	for character in characters:
		character = add_born_range(character)
	return characters


def sql_update_born_range_all_characters(characters):
	for character in characters:
		update_birth_range(character['id'], character['born_start'], character['born_end'])
	return "All Updated"


def update_born_range_all_characters():
	characters = pull_all_raw_born()
	characters = find_born_range_list_of_characters(characters)
	print sql_update_born_range_all_characters(characters)
