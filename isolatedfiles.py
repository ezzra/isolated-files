#!/usr/bin/env python

# Syntax: duplicates.py -s source_folder -t target_folder

import os
import sys
import glob
import argparse
import pprint
import subprocess
import re

pp = pprint.PrettyPrinter(width=500)

# argument parsing
parser = argparse.ArgumentParser(description='Find files that do not exist in the source folders but in the target folders.')
parser.add_argument('-s', '--source', dest='sources', action='append', help='set source folders', required=True)
parser.add_argument('-t', '--target', dest='targets', action='append', help='set target folders', required=True)
args = parser.parse_args()


def create_foundfiles(folders: list) -> dict:
    foundfiles = dict()
    files = list()
    for folder in folders:
        ssh = re.findall(r'([^\s/]+):(.*)', folder)
        if ssh:
            files += get_allfiles_ssh(ssh[0][0], ssh[0][1])
        else:
            files += get_allfiles(folder)

    for filepathname in files:
        merge_id = get_merge_id(filepathname)
        if merge_id not in foundfiles:
            foundfiles[merge_id] = list()
        foundfiles[merge_id].append(filepathname)

    return foundfiles


def get_allfiles(folder: str) -> list:
    """Returns all files from all subfolders as a list"""
    allfiles = list()
    for root, dirs, files in os.walk(folder):
        for file in files:
            allfiles.append(os.path.join(root, file))
    return allfiles


def get_merge_id(filepathname: str) -> str:
    """Returns an id of filename + filesize to identify files as duplicate"""
    filename = os.path.basename(filepathname).lower()
    size = os.stat(filepathname).st_size
    merge_id = filename + str(size)
    return merge_id


def get_allfiles_ssh(ssh_shortcut: str, folder: str) -> list:
    filenames = subprocess.check_output(
        'ssh %s find %s -type f' % (ssh_shortcut, folder or '.'),
        stderr=subprocess.STDOUT,
        timeout=30,
        shell=True,
        universal_newlines=True)
    allfiles = filenames.splitlines()
    return allfiles


# create dicts with merge_ids
found_sourcefiles = create_foundfiles(args.sources)
found_targetfiles = create_foundfiles(args.targets)

# get merge_ids that are not served in sources
missings = found_targetfiles.keys() - found_sourcefiles.keys()

# loop all missing files
for merge_id in missings:
    print('---')
    for filepathname in found_targetfiles[merge_id]:
        print(filepathname)






