# -*- coding: utf-8 -*-

""" Tablib - MD5 (MD5 List Files) Support.
"""

import sys
if sys.version_info[0] > 2:
    from io import StringIO
else:
    from cStringIO import StringIO
    
import csv
import os

import tablib


title = 'md5'
extentions = ('',)

def export_set(dataset):
    stream = StringIO()
    _tsv = csv.writer(stream, delimiter=' ')

    for row in dataset._package(dicts=False):
        _tsv.writerow(row)

    return stream.getvalue()


def import_set(dset, in_stream, headers=True):
    dset.wipe()

    rows = csv.reader(in_stream.splitlines(), delimiter=' ')
    for i, row in enumerate(rows):
        # Skip empty rows
        if not row:
            continue

        dset.append(row)


def detect(stream):
    """Returns True if given stream is valid TSV."""
    try:
        rows = dialect = csv.Sniffer().sniff(stream, delimiters=' ')
        return True
    except csv.Error:
        return False
