#!/usr/bin/env python

"""dam.py: Library to parse out text."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

"""
Requires shell commands:
- wkhtmltopdf
- pdftotext

"""
import re
from collections import defaultdict
import pdb

def read_line(line, keywords, pattern):
    """Processes line containing values for one attribute."""
    # TODO
    return

def get_slots_list(values, text):
    """Returns list mapping each index in text to its header value."""
    slots_list = [None] * (len(text) - 1)

    for value in values:
        start = text.lower().find(value.lower())
        end = start + len(value)
        slots_list[start:end] = [value] * len(value)

    return slots_list

def expand_list(lst, filled):
    """Expands non-None elements in a list to its adjacent None cells."""
    if not isinstance(lst, list):
        raise BaseException

    # Enum values
    IDX, VAL = 0, 1

    forward = backward = idx = None

    # Get the first non-None value in list
    forward = backward = next([idx, value]\
            for idx, value in enumerate(lst) if filled(value)) #value is not None)

    # Expand the first non-None value to beginning of list
    lst[0:forward[IDX]] = [forward[VAL]] * forward[IDX]

    # Iterate through elements, finding values to expand out
    # Initialize first forward value
    backward = forward
    for idx, value in enumerate(lst[forward[IDX]:], start=forward[IDX]):
        # Update forward index to be right before start of gap
        if not filled(value) and (backward is None or filled(backward[VAL])):
            forward[IDX] = idx - 1

        backward = [idx, value]

        if filled(forward[VAL]) and filled(backward[VAL])\
            and forward[VAL] != backward[VAL]:
            # Fill in gap if we find non-None value to expand backwards
            for offset in range(1, 1 + (backward[IDX] - forward[IDX]) / 2):
                lst[backward[IDX] - offset] = backward[VAL]
                lst[forward[IDX] + offset] = forward[VAL]

            # Resolve odd numbered gaps
            if (backward[IDX] - forward[IDX] - 1) % 2 == 1:
                lst[forward[IDX] + (backward[IDX] - forward[IDX]) / 2] = forward[VAL]

            # Set forward as backward; clear backward
            forward = backward
            backward = None

    # Expand last non-None value to end of list
    lst[(forward[IDX] + 1):] = [forward[VAL]] * (len(lst) - forward[IDX] - 1)

    return lst

def get_count_list(text):
    if not isinstance(text, str):
        raise BaseException

    counts_dict = defaultdict(int)
    pos = 0
    for char in text:
        if char != ' ':
            counts_dict[pos] += 1
        pos = 0 if char == '\n' else pos + 1

    counts_list = [0] * (1 + sorted(counts_dict.keys())[-1])
    for k, v in counts_dict.iteritems():
        counts_list[k] = v

    return counts_list

def parse_table(header, delimiter, text):
    """Processes textual table into multiple entities, entities being rows."""

    header_i = 0

    header_text = text[0:(text.find('\n') + 1)]
    body_text = text[text.find('\n') + 1:]
    body_rows = body_text.split('\n')

    # Maps character slots in a row to the header row value
    def get_name(x):
        return x['name']
    def not_none(x):
        return x is not None

    header_slots = get_slots_list(map(get_name, header), header_text)
    expand_list(header_slots, not_none)

    count_slots = get_count_list(body_text)

    # Get delimiter indices
    delimiter_indices = []
    walker = -1
    for idx, value in enumerate(count_slots):
        if value == 0 and walker != 0:
            delimiter_indices.append(idx)
        walker = value
    delimiter_indices.append(len(count_slots) - 1)

    # Split each text row into an array of values
    def split_row(row, delimiter_indices):
        return [row[i:j] for i, j in zip(delimiter_indices[:-1], delimiter_indices[1:])]
    body_rows = [split_row(row, delimiter_indices) for row in body_rows]

    # Transpose body_rows so we have a list of lists, each inner list being values of same type
    body_rows = [list(tpl) for tpl in zip(*body_rows)]

    # Expand out values in lists to fill empty cells
    def not_spaces(x):
        return True if x.strip() != '' else False
    body_rows = [expand_list(row, not_spaces) for row in body_rows]

    # Transpose body_rows inner lists contain values for one doc
    body_rows = [list(tpl) for tpl in zip(*body_rows)]
    for row in body_rows:
        print row

    # Create array of just header labels
    def get_name(x):
        return x['name']
    labels = map(get_name, header)

    # Create array of dicts using body_rows
    def strip(x):
        return x.strip()
    def list_to_dict(x, labels, strip):
        return {k:v for k, v in zip(labels, map(strip, x))}
    collection = [list_to_dict(row, labels, strip) for row in body_rows]

    for doc in collection:
        print doc

    # TODO: Fill empty cells

    # TODO: Read lines as rows

        # TODO: Break down rows into pieces

    return
