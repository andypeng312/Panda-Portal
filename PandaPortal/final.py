#!/usr/bin/env python
import os
import sys
import resource
from runinbg import *

def PandaPortalProgram():
    import main
    main.runPandaPortal()

def errorWindow():
    import UnexpectedErrors
    UnexpectedErrors.ErrorWindow()

def runSequence():
    f1 = lambda: os._exit(0)
    f2 = lambda: runInBackground(PandaPortalProgram, errorWindow,
                                 os.path.dirname(sys.argv[0]))
    runInBackground(f1, f2, os.path.dirname(sys.argv[0]))

runSequence()