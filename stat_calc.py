import re

from config import get_main_configurations
from log import log
from sql import pull_all_raw_born, update_birth_range


def clean_numbers(raw_numbers):
    return [int(n) for n in raw_numbers]


def value_extractor(born_string, extract_style):
    shift = int(configs['rough_shift'])

    if extract_style == 'only':
        numbers = re.findall(r'\b\d+\b', born_string)
        numbers = clean_numbers(numbers)
        return (numbers[0], numbers[0], numbers[0], numbers[0])

    if extract_style == 'only_roughly':
        numbers = re.findall(r'\b\d+\b', born_string)
        numbers = clean_numbers(numbers)
        return (numbers[0], numbers[0], numbers[0]-shift, numbers[0]+shift)

    if extract_style == 'only_negative':
        numbers = re.findall(r'\b\d+\b', born_string)
        numbers = clean_numbers(numbers)
        return (numbers[0] * -1, numbers[0] * -1,
                numbers[0] * -1, numbers[0] * -1)

    if extract_style == 'first_second':
        numbers = re.findall(r'\b\d+\b', born_string)
        numbers = clean_numbers(numbers)
        return (min(numbers), max(numbers), min(numbers), max(numbers))


    if extract_style == 'first_second_roughly':
        numbers = re.findall(r'\d+', born_string)
        numbers = clean_numbers(numbers)
        exact = (min(numbers), max(numbers))
        numbers.append((min(numbers) - shift))
        numbers.append((max(numbers) + shift))
        rough = (min(numbers), max(numbers))
        return (exact[0], exact[1], rough[0], rough[1])


    if extract_style == 'first_neg_second_neg':
        numbers = re.findall(r'\d+', born_string)
        numbers = clean_numbers(numbers)
        return (max(numbers) * -1, min(numbers) * -1,
                max(numbers) * -1, min(numbers) * -1)

    if extract_style == 'in_or_after':
        numbers = re.findall(r'\d+', born_string)
        numbers = clean_numbers(numbers)
        return (min(numbers), "NULL", min(numbers), "NULL")

    if extract_style == 'in_or_before':
        numbers = re.findall(r'\d+', born_string)
        numbers = clean_numbers(numbers)
        return ("NULL", max(numbers), "NULL", max(numbers))

    if extract_style == 'in_or_before_roughly':
        numbers = re.findall(r'\d+', born_string)
        numbers = clean_numbers(numbers)
        return ("NULL", max(numbers), "NULL", max(numbers) + shift)

    return ("NULL", "NULL")


def collect_templates():

    templates = dict()

    templates[r'\AIn (\d{1,3} AC \(roughly\)|or around \d{1,3} AC)(\Z|, at )'] = "only_roughly"
    templates[r'\AIn (about|or around) \d{1,3} AC(?: \(roughly\))?(\Z|, at )'] = "only_roughly"

    templates[r'\A(?:At |In )?(?:or )?(?:between )?\d{1,3} AC (and|or) \d{1,3} AC(\Z|, at )'] = 'first_second'
    templates[r'\A(In|At) (?:either |or around )?\d{1,3} AC, \d{1,3} AC or \d{1,3} AC(\Z|, at )'] = 'first_second'

    templates[r'\AIn \d{1,3}(?: )?AC or (after|later)(\Z|, at )'] = "in_or_after"
    templates[r'\AIn After \d{1,3} AC(\Z|, at )'] = "in_or_after"

    templates[r'\A(?:In |At )?\d{1,3} AC(\Z|, at )'] = "only"
    templates[r'\AIn or between (~\d{1,3} AC and \d{1,3} AC|\d{1,3} AC and \d{1,3} AC \(roughly\))(\Z|, at )'] = "first_second_roughly"
    templates[r'\A(?:In )?(or before \d{1,3} AC|\d{1,3} AC or before)(\Z|, at )'] = "in_or_before"
    templates[r'\AIn \d{1,3} AC or before \(roughly\)(\Z|, at )'] = "in_or_before_roughly"
    templates[r'\A\d{1,3} BC(\Z|, at )'] = "only_negative"
    templates[r'\AIn \d{1,3}BC or \d{1,3}BC(\Z|, at )'] = "first_neg_second_neg"

    return templates


def born_parser(born_string):
    templates = collect_templates()
    if born_string is not None:
        for key in templates.keys():
            if re.match(key, born_string):
                return value_extractor(born_string, templates[key])
    return (None, None, None, None)


def num_there(s):
    return any(i.isdigit() for i in s)


def add_born_range(character):
    birth_range = born_parser(character['born'])
    character['born_start_pre_rough'] = birth_range[0]
    character['born_end_pre_rough'] = birth_range[1]
    character['born_start'] = birth_range[2]
    character['born_end'] = birth_range[3]
    if character['born'] is not None and num_there(character['born']) and birth_range == (None, None, None, None):
        log(character['born'])
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
    log(sql_update_born_range_all_characters(characters))


configs = get_main_configurations()
