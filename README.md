# isolated-files
find isolated files with no duplicate between multiple folders

simple script that I use to find files that **do not** exist in source-folders but **do exist** in target folders. So its like searching for non-duplicates.

```
folder1
- file1.txt
- file2.txt
- file3.txt

folder2
- file1.txt
- file2.txt
- file4.txt
```

```
$ isolated-files.py -s folder1 -t folder2
#/folder2/file4.txt
```

- you can use multiple source or target folders
- you can also use an ssh folder like `-s myserver:folder1` where _myserver_ must be configured as host in ssh config
