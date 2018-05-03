import re

from config import get_main_configurations
from log import log


class born_extractor:
    def __init__(self):
        self.names = ['extract_only', 'extract_only_roughly',
                      'extract_only_negative', 'extract_first_second',
                      'extract_first_second_roughly',
                      'extract_first_neg_second_neg',
                      'extract_in_or_after', 'extract_in_or_before'
                     ]
        self.templates = dict()
        self.templates['extract_only'] = re.compile(
        r"""(?:In |At )?\d{1,3} AC(\Z|, at )"""
        )

        self.templates['extract_only_roughly'] = re.compile(
        r"""(?:In )?((?:or around )?\d{1,3} AC \(roughly\)|(?:In )?(about|or around) \d{1,3} AC)(\Z|, at )"""
        )

        self.templates['extract_only_negative'] = re.compile(
        r"""(?:In )?\d{1,3} BC(\Z|, at )"""
        )

        self.templates['extract_first_second'] = re.compile(
        r"""(?:In |At )?(?:or between |either )?\d{1,3}(?: AC)?(?:, \d{1,3} AC)? (and|or) \d{1,3} AC(\Z|, at )"""
        )

        self.templates['extract_first_second_roughly'] = re.compile(
        r"""(?:In )?(?:or between )?~\d{1,3} AC(?:, \d{1,3} AC)? (and|or) \d{1,3} AC(\Z|, at )"""
        )

        self.templates['extract_first_neg_second_neg'] = re.compile(
        r"""(?:In )?\d{1,3}BC or \d{1,3}BC(\Z|, at )"""
        )

        self.templates['extract_in_or_after'] = re.compile(
        r"""(?:In )?(\d{1,3} AC or (after|later)|After \d{1,3} AC)(\Z|, at )"""
        )

        self.templates['extract_in_or_before'] = re.compile(
        r"""(?:In )?(\d{1,3} AC or before|or before \d{1,3} AC)(\Z|, at )"""
        )

        self.extracts = dict()
        def extract_only(born_string):
            numbers = re.findall(r'\b\d+\b', born_string)
            return (numbers[0], numbers[0], numbers[0], numbers[0])
        self.extracts['extract_only'] = extract_only


        def extract_only_roughly(born_string):
            numbers = re.findall(r'\b\d+\b', born_string)
            numbers = clean_numbers(numbers)
            return (numbers[0], numbers[0], numbers[0] - configs['shift'],
                    numbers[0] + configs['shift'])
        self.extracts['extract_only_roughly'] = extract_only_roughly


        def extract_only_negative(born_string):
            numbers = re.findall(r'\b\d+\b', born_string)
            numbers = clean_numbers(numbers)
            return (numbers[0] * -1, numbers[0] * -1,
                    numbers[0] * -1, numbers[0] * -1)
        self.extracts['extract_only_negative'] = extract_only_negative


        def extract_first_second(born_string):
            numbers = re.findall(r'\b\d+\b', born_string)
            numbers = clean_numbers(numbers)
            return (min(numbers), max(numbers), min(numbers), max(numbers))
        self.extracts['extract_first_second'] = extract_first_second


        def extract_first_second_roughly(born_string):
            numbers = re.findall(r'\d+', born_string)
            numbers = clean_numbers(numbers)
            exact = (min(numbers), max(numbers))
            numbers.append((min(numbers) - configs['shift']))
            numbers.append((max(numbers) + configs['shift']))
            rough = (min(numbers), max(numbers))
            return (exact[0], exact[1], rough[0], rough[1])
        self.extracts['extract_first_second_roughly'] = extract_first_second_roughly


        def extract_first_neg_second_neg(born_string):
            numbers = re.findall(r'\d+', born_string)
            numbers = clean_numbers(numbers)
            return (max(numbers) * -1, min(numbers) * -1,
                    max(numbers) * -1, min(numbers) * -1)
        self.extracts['extract_first_neg_second_neg'] = extract_first_neg_second_neg


        def extract_in_or_after(born_string):
            numbers = re.findall(r'\d+', born_string)
            numbers = clean_numbers(numbers)
            return (min(numbers), "NULL", min(numbers), "NULL")
        self.extracts['extract_in_or_after'] = extract_in_or_after


        def extract_in_or_before(born_string):
            numbers = re.findall(r'\d+', born_string)
            numbers = clean_numbers(numbers)
            return ("NULL", max(numbers), "NULL", max(numbers))
        self.extracts['extract_in_or_before'] = extract_in_or_before


        def extract_in_or_before_roughly(born_string):
            numbers = re.findall(r'\d+', born_string)
            numbers = clean_numbers(numbers)
            return ("NULL", max(numbers), "NULL", max(numbers) + configs['shift'])
        self.extracts['extract_in_or_before_roughly'] = extract_in_or_before_roughly


def clean_numbers(raw_numbers):
    return [int(n) for n in raw_numbers]


def born_parser(born_string):
    numFlag = False
    if num_there(born_string):
        numFlag = True
        born_parser = born_extractor()
        for key in born_parser:
            if re.match(born_parser.templates[key], born_string):
                return born_parser.extracts[key](born_string)
        if numFlag:
            print "No match: {}".format(born_string)
    return (None, None, None, None)


def num_there(s):
    if s == None:
        return False
    return any(i.isdigit() for i in s)


def add_born_range(character):
    birth_range = born_parser(character['born'])
    character['born_start_pre_rough'] = birth_range[0]
    character['born_end_pre_rough'] = birth_range[1]
    character['born_start'] = birth_range[2]
    character['born_end'] = birth_range[3]
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
