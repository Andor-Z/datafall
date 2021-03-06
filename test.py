#!/usr/bin/env python

"""test.py: Tests for Clearstream library."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

import clearstream
import dam
import waterfall
import bridge
import os
import re
from pymongo import MongoClient

client = MongoClient()
db = client['test-database']

def test_clearstream():
    """Used to test functionality of clearstream.py."""

    temp_dir_path = clearstream.temp_dir_path
    if not os.path.exists(temp_dir_path):
        os.makedirs(temp_dir_path)

    sources = [
        ('http://www.iwf.net/results/results-by-events/?event=313', temp_dir_path + '2015EuropeanChampionships'),
        ('samples/Results_Book_Almaty2014.pdf', temp_dir_path + 'Results_Book_Almaty2014'),
        ('http://espn.go.com/college-football/player/_/id/529898/tyler-varga', temp_dir_path + 'varga-espn-profile'),
        ('sample_pdfs/varga-espn-profile.pdf', temp_dir_path + 'varga-espn-profile')
    ]

    clearstream.create_txt_from_pdf(*sources[3])

def import_iwf_results():

    mens_results_header = [
        dict(name='category', pattern='\d{2,3}+?'),
        dict(name='lift', pattern='snatch|clean|jerk', ignore_case=True),
        dict(name='rank', pattern='\d{1}'),
        dict(name='result', pattern='\d+'),
        dict(name='name', pattern='(\w+ ?)+'),
        dict(name='born', pattern='(\d\.),+'),
        dict(name='nation', pattern='[a-z]+', ignore_case=True)
    ]

    lifts_dict = {
        'Snatch' : 'snatch',
        'C&Jerk' : 'cleanjerk',
        'Total' : 'total'
    }
    def convert_lift(original):
        original['lift'] = lifts_dict[original['lift']]
        return original

    results = [dam.parse_text_table(mens_results_header, '  ', open('temp/womens-results.txt', 'r').read()),
               dam.parse_text_table(mens_results_header, '  ', open('temp/mens-results.txt', 'r').read())]

    for result in results:
        athletes = [bridge.filter_dict(athlete, ('name', 'born', 'nation')) for athlete in result]
        waterfall.insert_into_db('athletes', athletes)

        lifts = [bridge.filter_dict(lift, ('name', 'born', 'nation', 'lift', 'result', 'rank', 'category')) for lift in result]
        lifts = [bridge.link('athletes', 'athlete_id', ['name', 'born', 'nation'], lift) for lift in lifts]
        # TODO: This conversion should be handled automatically, i.e. standardization of values
        lifts = [convert_lift(lift) for lift in lifts]
        waterfall.insert_into_db('lifts', lifts)

def import_usaw_results():
    results = dam.parse_csv_table('sample_pdfs/oklahoma-meet-results-processed.csv')
    athletes = [bridge.filter_dict(athlete, collection='athletes') for athlete in results]
    waterfall.insert_into_db('athletes', athletes)

    lifts = [bridge.filter_dict(lift, keys=['name', 'bodyweight', 'snatch', 'cleanjerk', 'total', 'event', 'date']) for lift in results]

    # Split lifts into three docs for snatch, clean and jerk, and total
    snatches = [bridge.filter_dict(lift, keys=['name', 'bodyweight', 'snatch', 'event', 'date']) for lift in lifts]
    for snatch in snatches:
        snatch['lift'] = 'snatch'
        snatch['result'] = snatch['snatch']
        del snatch['snatch']

    cleanjerks = [bridge.filter_dict(lift, keys=['name', 'bodyweight', 'cleanjerk', 'event', 'date']) for lift in lifts]
    for cleanjerk in cleanjerks:
        cleanjerk['lift'] = 'cleanjerk'
        cleanjerk['result'] = cleanjerk['cleanjerk']
        del cleanjerk['cleanjerk']

    totals = [bridge.filter_dict(lift, keys=['name', 'bodyweight', 'total', 'event', 'date']) for lift in lifts]
    for total in totals:
        total['lift'] = 'total'
        total['result'] = total['total']
        del total['total']

    lifts = snatches + cleanjerks + totals
    lifts = [bridge.link('athletes', 'athlete_id', ['name'], lift) for lift in lifts]
    waterfall.insert_into_db('lifts', lifts)

def clean_database():
    """Clean database"""
    db['athletes'].remove({})
    db['lifts'].remove({})
    db['events'].remove({})

def main():
    test_clearstream()
    # clean_database()
    # import_iwf_results()
    # import_usaw_results()

if __name__ == '__main__':
    main()
