#!/usr/bin/env python

import shutil
import sys
import os
from MakeChanges import *

def shareFile():
    fullTxt = Settings().readSets()
    LocalDirectory = re.search('(?<=Local Directory: ).+', fullTxt).group()
    fileToMove = sys.argv[1]
    dest = "%s/%s" % (LocalDirectory, os.path.basename(fileToMove))
    shutil.move(fileToMove, dest)
    os.symlink(dest, fileToMove)

os.chdir(os.path.dirname(sys.argv[0]))
shareFile()