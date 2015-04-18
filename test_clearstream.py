#!/usr/bin/env python

"""clearstream_test.py: Tests for Clearstream library."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

import clearstream
import os

def main():
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

if __name__ == '__main__':
    main()
