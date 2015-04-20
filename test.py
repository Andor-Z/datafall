#!/usr/bin/env python

"""test.py: Tests for Clearstream library."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

import clearstream
import dam
import os
import re

def test_clearstream():
    temp_dir_path = clearstream.temp_dir_path

    """Used to test functionality of clearstream.py."""
    if not os.path.exists(temp_dir_path):
        os.makedirs(temp_dir_path)
    # create_txt_from_url('www.drudgereport.com', temp_dir_path + 'drudge_report.bad')
    # create_txt_from_url('http://status.rilin.state.ri.us/legislative_committee_calendar.aspx',
    #                     temp_dir_path + 'ri_events')
    # create_txt_from_url('https://twitter.com/a16z', temp_dir_path + 'a16z.txt')
    clearstream.create_txt_from_url('http://www.iwf.net/results/olympic-records/', temp_dir_path + 'mens_olympic_records_2')
    clearstream.create_txt_from_pdf('samples/Results_Book_Almaty2014.pdf')

def test_dam():
    mens_results_header = [
        dict(name='category', pattern='\d{2,3}+?'),
        dict(name='lift', pattern='snatch|clean|jerk', ignore_case=True),
        dict(name='rank', pattern='\d{1}'),
        dict(name='result', pattern='\d+'),
        dict(name='name', pattern='(\w+ ?)+'),
        dict(name='born', pattern='(\d\.),+'),
        dict(name='nation', pattern='[a-z]+', ignore_case=True)
    ]

    dam.parse_table(mens_results_header, '  ', open('samples/mens-results.txt', 'r').read())

def main():
    # test_clearstream()
    test_dam()

if __name__ == '__main__':
    main()