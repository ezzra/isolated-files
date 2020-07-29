# isolated-files
find isolated files with no duplicate between multiple folders

simple script that I use to find files that **do not** exist in source-folders but **do exist** in target folders. So its like searching for non-duplicates.

- it will compare files only based on filename and filesize (that was intended because I had to work with very large files)
- it work recursively, not depending on the pathes where files are stored in
- you can use multiple source or target folders (just `--target folder2 --target folder3`)
- you can also use an ssh folder for example `--source myserver:folder1` where _myserver_ must be configured as host in ssh config
- there isn't any writing command used, so you can use it without fear of data loss (but of course, I wont take any responsibility)

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

folder3
- file2.txt
```

#### Usage
```
$ isolated-files.py --source folder1 --target folder2 --target folder3
#/folder2/file4.txt
```

you can use `-l /copy/folder/path` to specify a folder where the found files are hardlinked to
