#!/usr/bin/env python

import time
import sys
import os
from MakeChanges import *

class Log(object):
    maxLines = 100
    def __init__(self):
        self.log = "log.txt"
        if not os.path.exists(self.log):
            open(self.log, "wb").close()

    def write(self, string):
        f = open(self.log, "rb")
        linesList = f.read().split("\n")
        f.close()
        linesList.append(string)
        if (len(linesList) > Log.maxLines):
            i = len(linesList) - Log.maxLines
            linesList = linesList[i:len(linesList)]
        data = "\n".join(linesList)
        f = open(self.log, "wb")
        f.seek(0)
        f.write(data)
        f.close()

def main(login, timesPer10Minutes):
    while True:
        t0 = time.time()
        cycleLen = 600 / timesPer10Minutes # min = 5, max = 600
        change_update_cycle(login.SSH)
        tf = time.time()
        elapsed = tf - t0
        if (elapsed < cycleLen):
            time.sleep(cycleLen - elapsed)