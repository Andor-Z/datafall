#!/usr/bin/env python

"""bridge.py: Library to use database queries to identify entities in input."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

"""
Given a dictionary input, we should try to match key names to keys in a MongoDB database or rows in a Postgres database.
"""

# TODO: Implement search tool to identify matching names with names in database.

from pymongo import MongoClient

client = MongoClient()
db = client['test-database']

def filter_dict(dictionary, keys, invert=False):
    """Filters a dict, keeping only certain keys but creates a new dict."""

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
