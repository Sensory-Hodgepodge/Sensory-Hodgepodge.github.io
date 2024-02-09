import json
import os

current_file_path = os.path.abspath(__file__)
current_file_directory = os.path.dirname(current_file_path)


def get_attributes():
    with open(f'{current_file_directory}/db/attributes.json', 'r') as file:
        data = json.load(file)
    return data['attributes']


def get_attributes_and_names():
    modified_attributes = {}
    for attr in get_attributes():
        modified_key = attr.replace('_', ' ').capitalize()
        modified_attributes[attr] = modified_key

    return modified_attributes


class Song:
    def __init__(self, **kwargs):
        attributes = get_attributes()
        for attr in attributes:
            setattr(self, attr, kwargs.get(attr, None))

    def to_dict(self):
        song_dict = {}
        attributes = get_attributes()
        for attr in attributes:
            song_dict[f'{attr}'] = getattr(self, f'{attr}')
        return song_dict
