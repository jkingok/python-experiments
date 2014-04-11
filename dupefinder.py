#!/usr/bin/env python

from os import walk
import os.path
import stat

# Master list of found files
files = {}

# checks whethere the file is suitable
def candidate(path):
    s = os.stat(path)
    return stat.S_ISREG(s.st_mode)

# constructs as much info about a file as possible
def identify(path):
    return {'path': os.path.split(path)[0],
        'name': os.path.splitext(os.path.split(path)[1])[0],
        'ext': os.path.splitext(os.path.split(path)[1])[1]}

# callback for walking through directories
def walker(arg, dirname, filenames):
    for filename in filenames:
        pathfile = os.path.join(dirname, filename)
        if candidate(pathfile):
            files[pathfile] = identify(pathfile)

# split the given list into a list of lists where the items are distinct
def separate(items):
    names = {}
    for k, v in l.items():
        filename = v['name'] + v['ext']
        if filename in names:
            names[filename][k] = v
        else:
            names[filename] = {k: v}
    return names.values()

# main logic
# Old way
#os.path.walk(".", walker, u"Walker")
# New way
for root, dirs, names in os.walk("."):
    walker(u"Walker", root, names)

# progressively whittle down the list
# initial assumption: everything is the same
whittled = [files]

# rule 1 - files with the same name are the same
nextw = []
for l in whittled:
    if len(l) > 1:
        nextw += separate(l)
whittled = [ x for x in nextw if len(x) > 1 ]

# print result
#for x in whittled:
#    print x

# or a summary
print("From", len(files), "file(s) scanned:")
n = sum([ len(x) for x in whittled ])
print(n, "duplicate files in", len(whittled), "set(s)")
print(len(files) - n, "or", 100 - float(n) / len(files) * 100, "% were unique.")
if n > 0:
    print("Duplicates:")
    for i, f in enumerate(whittled):
        print(i + 1, list(f.keys()))
