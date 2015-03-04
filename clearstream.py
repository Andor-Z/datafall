#!/usr/bin/env python

"""clearstream.py: Library to converts web pages into text files with layout."""

__author__      = 'Earl Lee'
__copyright__   = 'Copyright 2015'

import os
import subprocess
import re
import pdb

path_re = re.compile('(.*/)?(.*)(\..*)?')
temp_dir_path = 'temp/'

def url_to_pdf(url):
    """Creates a PDF printout of a web page at URL."""
    try:
        FNULL = open(os.devnull, 'w') # used to pipe stderr into /dev/null
        proc = subprocess.Popen(['wkhtmltopdf', url, '-'], stdout=subprocess.PIPE,
                                stderr=FNULL, close_fds=True)
    except OSError as e:
        raise EnvironmentError('Error: convertPDF() failed.\n%s' % e)

    data = proc.stdout.read()
    proc.stdout.close()
    return data

def pdf_to_text(data):
    """Runs a file through pdftotext command and returns the text."""
    try:
        FNULL = open(os.devnull, 'w') # used to pipe stderr into /dev/null
        proc = subprocess.Popen(['pdftotext', '-layout', '-', '-'], stdout=subprocess.PIPE,
                                stderr=FNULL, stdin=subprocess.PIPE, close_fds=True)
        proc.stdin.write(data)
        proc.stdin.close()
    except OSError as e:
        raise EnvironmentError('Error: convertPDF() failed.\n%s' % e)

    data = proc.stdout.read()
    proc.stdout.close()
    return data

def url_to_text(url):
    """Gets text of a web page at URL."""
    return pdf_to_text(url_to_pdf(url))

def write_file(data, path):
    """Writes data to file at path."""
    f = open(path, 'w')
    f.write(data)
    f.close()

def read_file(path):
    """Reads file data at and returns it."""
    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

def create_pdf_from_url(url, output_path=temp_dir_path + 'out.txt'):
    """Creates PDF file from a webpage at URL using wkhtmltopdf command."""
    write_file(url_to_pdf(url), output_path)

def create_txt_from_pdf(data, output_path=temp_dir_path + 'out.txt'):
    """Creates text file by converting PDF data into text with pdftotext command."""
    write_file(pdf_to_text(data), output_path)

def create_txt_from_url(url, output_path=temp_dir_path + 'out.txt'):
    """
    Creates text file of web page text from URL source.

    First loads URL as web page. Converts web page to a PDF with wkhtmltopdf
    command. Then converts PDF into text with pdftotext command. Does not create
    temporary files.
    """
    write_file(url_to_text(url), output_path)

def main():
    """Used to test functionality of clearstream.py."""
    if not os.path.exists(temp_dir_path):
        os.makedirs(temp_dir_path)
    create_txt_from_url('www.drudgereport.com')

if __name__ == '__main__':
    main()
