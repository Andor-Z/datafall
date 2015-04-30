#!/usr/bin/env python

"""bridge.py: Library to use database queries to identify entities in input."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

"""
Given a dictionary input, we should try to match key names to keys in a MongoDB database or rows in a Postgres database.
"""

from pymongo import MongoClient
from fuzzywuzzy import process

client = MongoClient()
db = client['test-database']

def filter_dict(dictionary, keys=None, invert=False, collection=None, match_threshold=50):
    """Filters a dict, keeping only certain keys but creates a new dict."""

    # If a target collection name is passed in, use that collection to set the keys
    if collection is not None:
        def reducer(all_keys, rec_keys):
            return all_keys | set(rec_keys)
        def get_keys(d):
            return d.keys()

        keys = reduce(reducer, map(get_keys, db[collection].find()), set())

    # Fuzzy match standard keys to to keys in dictionary by replacing key names
    # in dictionary with standard key names
    dict_keys = dictionary.keys()
    for key in keys:
        # Match desired collection key to a key in incoming dictionary and
        # change the name in dictionary
        matches = process.extract(key, dict_keys)
        for match in matches:
            if match[0] == key:
                continue
            elif match[1] > match_threshold:
                dictionary[key] = dictionary[match[0]]
                del dictionary[match[0]]
                break

    # Filter modified dictionary using keys
    if invert:
        for key in keys:
            dictionary.pop(key, None)
    else:
        key_set = set(keys) & set(dictionary.keys())
        dictionary = {k: dictionary[k] for k in key_set}

    return dictionary

def link(collection_name, ref_key, match_keys, payload):
    collection = db[collection_name]

    search_dict = filter_dict(payload, match_keys)
    match = collection.find_one(search_dict)
    match_id = match['_id']
    if match_id:
        payload = filter_dict(payload, match_keys, invert=True)
        payload[ref_key] = match_id
    else:
        # TODO: Test this branch
        return None

    return payload

def clean_payload(keys, payload):
    return payload
