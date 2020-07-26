# isolated-files
find isolated files with no duplicate between multiple folders

simple script that I use to find files that **do not** exist in source-folders but **do exist** in target folders. So its like searching for non-duplicates.

#### Example
```
folder1
- file1.txt
- file2.txt
- file3.txt # this file is only in folder1

folder2
- file1.txt
- file2.txt
- file4.txt # this file is only in folder2
```

#### Usage
```
$ isolated-files.py --source folder1 --target folder2
#/folder2/file4.txt
```

- there is a distinction between source and target folders, so `file3.txt` is not in `folder2` but that doesn't matter
- you can use multiple source or target folders (just `--target folder2 --target folder3`)
- you can also use an ssh folder for example `--source myserver:folder1` where _myserver_ must be configured as host in ssh config
