#!/usr/bin/env python

import os
import sys
from SplashScreen import *
from UnexpectedErrors import *

def runPandaPortal():
    log = Log()
    errorLog = ErrorClass()
    sys.stdout = log
    sys.stderr = errorLog
    run()

#os.chdir("/Users/Andy/Desktop/Project")
#runPandaPortal()