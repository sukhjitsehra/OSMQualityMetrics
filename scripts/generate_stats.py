#!/usr/bin/python

import sys
import glob
from subprocess import call
import commands
import os
import shutil

osmjs_path = ""


def usage():
    print """
Usage: generate_stats in_dir out_dir [path_to_osmium]

in_dir contains one or more OSM files (.osm.pbf)
out_dir is where the stats CSVs will be written

Make sure that osmjs (part of osmium) is installed, osmjs is compiled, and in the current path (or pass path_to_osmium).
"""
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Too few arguments ({num}).".format(num=len(sys.argv) - 1)
        usage()
    osmjs_path = commands.getoutput("which osmjs")
    if osmjs_path == "":
        if len(sys.argv) == 4:
            osmjs_path = os.path.join(sys.argv[3], '/osmjs/osmjs')
            if not (os.path.isfile(osmjs_path) and os.access(osmjs_path, os.X_OK)):
                print "osmjs not in {inpath}".format(inpath=sys.argv[3])
    path = sys.argv[1]
    files = glob.glob(path + '*.osm.pbf')
    print 'will process {num} files'.format(num=len(files))
    for osmfile in files:
        basename = os.path.splitext(os.path.basename(osmfile))[0]
        call([osmjs_path, '-j' '../UserStats.js' '-l' 'array', osmfile])
        shutil.move('userstats.csv', os.path.join(sys.argv[2], basename + '.csv'))
