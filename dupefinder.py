#!/usr/bin/env python

from os import walk
import os.path
import stat

path = input('Enter the path to search:')

# Master list of found files
files = {}

# checks whether the file is suitable
def candidate(path):
    try:
        s = os.stat(path)
        return stat.S_ISREG(s.st_mode)
    except:
        return False

# constructs as much info about a file as possible
def identify(path):
    s = os.stat(path)
    return {'path': os.path.split(path)[0],
        'name': os.path.splitext(os.path.split(path)[1])[0],
        'ext': os.path.splitext(os.path.split(path)[1])[1],
        'size': s.st_size}

# callback for walking through directories
def walker(arg, dirname, filenames):
    for filename in filenames:
        pathfile = os.path.join(dirname, filename)
        if candidate(pathfile):
            files[pathfile] = identify(pathfile)

# split the given list into a list of lists where the items are distinct
def separate1(items):
    names = {}
    for k, v in items.items():
        filename = v['name'] + v['ext']
        if filename in names:
            names[filename][k] = v
        else:
            names[filename] = {k: v}
    return names.values()

def separate2(items):
    sizes = {}
    for k, v in items.items():
        if v['size'] in sizes:
            sizes[v['size']][k] = v
        else:
            sizes[v['size']] = {k: v}
    return sizes.values()

# main logic
# Old way
#os.path.walk(".", walker, u"Walker")
# New way
for root, dirs, names in os.walk(path):
    walker(u"Walker", root, names)

# progressively whittle down the list
# initial assumption: everything is the same
whittled = [files]

# rule 1 - files with the same name are the same
for rule in [ separate1, separate2 ]:
    nextw = []
    for l in whittled:
        if len(l) > 1:
            nextw += rule(l)
    whittled = [ x for x in nextw if len(x) > 1 ]

# print result
#for x in whittled:
#    print x

# or a summary
if len(files) > 0:
    print("From", len(files), "file(s) scanned:")
    n = sum([ len(x) for x in whittled ])
    print(n, "duplicate files in", len(whittled), "set(s)")
    print(len(files) - n, "or", 100 - float(n) / len(files) * 100, "% were unique.")
    if n > 0:
        print("Duplicates:")
        for i, f in enumerate(whittled):
            print(i + 1, list(f.keys()))
else:
    print("No files found!")
