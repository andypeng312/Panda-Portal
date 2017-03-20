#!/usr/bin/env python
import os
import sys
import resource

def runInBackground(f1, f2, dir):
    procId = os.fork() # binary fission
    if (procId > 0): # if original process
        f1()
    elif (procId == 0): # spawned process
        os.setsid()
        os.chdir(dir)
        os.umask(0)
        os.closerange(0, resource.RLIMIT_NOFILE)
        sys.stdin = os.open(os.devnull, os.O_RDONLY)
        sys.stdout = os.open(os.devnull, os.O_RDWR)
        sys.stderr = os.open(os.devnull, os.O_RDWR)
        f2()