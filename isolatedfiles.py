#!/usr/bin/env python

# Syntax: duplicates.py DIRECTORY DIRECTORY DIRECTORY ...

import os
import sys
import glob
import argparse
import pprint

pp = pprint.PrettyPrinter(width=500)


def create_foundfiles(files):
    foundfiles = dict()

    for filepathname in files:

        # todo is nur der basename ohne ext?
        filename = os.path.basename(filepathname).lower()
        size = os.stat(filepathname).st_size
        merge_id = filename + str(size)

        # merge_id appears for first time within this folder
        if merge_id not in foundfiles:
            foundfiles[merge_id] = list()

        # add this filepath to merge_id of this folder
        foundfiles[merge_id].append(filepathname)

    return foundfiles


# argument parsing
parser = argparse.ArgumentParser(description='Find files that do not exist in the source folders but in the target folders.')
parser.add_argument('-s', '--source', dest='sources', action='append', help='set source folders', required=True)
parser.add_argument('-t', '--target', dest='targets', action='append', help='set target folders', required=True)
args = parser.parse_args()

# collect sourcefiles and targetfiles
sourcefiles = list()
targetfiles = list()
for folder in args.sources:
    sourcefiles += glob.glob(os.path.join(folder, "**", "*.*"), recursive=True)
for folder in args.targets:
    targetfiles += glob.glob(os.path.join(folder, "**", "*.*"), recursive=True)

# create dicts with merge_ids
found_sourcefiles = create_foundfiles(sourcefiles)
found_targetfiles = create_foundfiles(targetfiles)

# get merge_ids that are not served in sources
missings = found_targetfiles.keys() - found_sourcefiles.keys()

# loop all missing files
for merge_id in missings:
    print('---')
    for filepathname in found_targetfiles[merge_id]:
        print(filepathname)






