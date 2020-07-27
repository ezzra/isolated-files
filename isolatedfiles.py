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
parser = argparse.ArgumentParser(description='Find files that do not exist in the source folders but in the target folders (call it anti-duplicates).')
parser.add_argument('-s', '--source', dest='sources', action='append', help='set source folders (use myhost:foldername for remote ssh connections)', required=True)
parser.add_argument('-t', '--target', dest='targets', action='append', help='set target folders (use myhost:foldername for remote ssh connections)', required=True)
args = parser.parse_args()


def create_foundfiles(folders: list) -> dict:
    foundfiles = dict()
    files = list()
    for folder in folders:
        ssh = re.findall(r'([^\s/]+):(.*)', folder)
        if ssh:
            files += get_allfiles(ssh[0][1] or '.', ssh[0][0])
        else:
            files += get_allfiles(folder)

    for filedatastring in files:
        merge_id = get_merge_id(filedatastring)
        if merge_id not in foundfiles:
            foundfiles[merge_id] = list()
        filepathname = re.findall(r"\{(\d+)\}(.+)", filedatastring)
        foundfiles[merge_id].append(filepathname[0][1])

    return foundfiles


def get_merge_id(filepathname: str) -> str:
    """Returns an id of filename + filesize to identify files as duplicate"""
    filedata = re.findall(r"\{(\d+)\}(.+)", filepathname)
    filename = os.path.basename(filedata[0][1]).lower()
    merge_id = filename + filedata[0][0]
    return merge_id


def get_allfiles(folder: str, ssh_shortcut: str = None) -> list:
    """Returns all files from all subfolders as a list"""
    ssh_string = 'ssh {} '.format(ssh_shortcut) if ssh_shortcut else ''
    cmd = '{}find {} -type f -printf "{{%k}}%p\\n"'.format(ssh_string, folder or '.')
    filenames = subprocess.check_output(
        cmd,
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



