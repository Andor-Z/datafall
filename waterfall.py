#!/usr/bin/env python

"""waterfall.py: Library to transform Python dictionaries to fit schema."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

"""
waterfall.py calls on bridge.py to structure the input data to fit the database's schema.
Once the input data is structured and validated, waterfall.py inserts that data into the database.
"""

import bridge
import logging
from pymongo import MongoClient

client = MongoClient()
db = client['test-database']
logger = logging.getLogger()

def insert_into_db(collection_name, payload, filter_keys=None):
    collection = db[collection_name]
    for doc in payload:
        doc = doc if filter_keys is None else bridge.filter_dict(doc, filter_keys)
        collection.update_one(doc, {'$set': doc}, upsert=True)
    return
