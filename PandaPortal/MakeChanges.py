#!/usr/bin/env python
import os
import time
import re
import datetime
from Data import *
from Files import *
from passwordPrompt import *

class Settings():

    settingsFile = ".config/settings"
    localFiles = ".config/LocalFiles"
    remoteFiles = ".config/RemoteFiles"

    def __init__(self):
        self.sets = Files(os.path.abspath(Settings.settingsFile))
        self.loc = Files(os.path.abspath(Settings.localFiles))
        self.rem = Files(os.path.abspath(Settings.remoteFiles))
    def readSets(self):
        return self.sets.readFromFile()
    def readLoc(self):
        return self.loc.readFromFile()
    def readRem(self):
        return self.rem.readFromFile()

def makeRemoteChanges(ssh):
    fullTxt = Settings().readSets()
    LocalDirectory = re.search('(?<=Local Directory: ).+', fullTxt).group()
    RemoteDirectory = re.search('(?<=Remote Directory: ).+', fullTxt).group()
    statsFile = Settings().readLoc()
    if (statsFile == ""):
        Settings().loc.writeToFile(dict())
    oldStats = statsFile
    dataFile = Data(LocalDirectory, "L", SSH = ssh)
    currentStats = dataFile.dict
    change = dataFile.compareChanges()
    for cat in change:
        for filename in change[cat]:
            fullPath = "%s/%s" % (LocalDirectory, filename)
            dest = "%s/%s" % (RemoteDirectory, filename)
            if ((cat == "Deleted") or (cat == "Modded")):
                if Files.exists(dest, "R"):
                    f = Files(dest, "R", SSH = ssh)
                    f.delete()
            if ((cat == "Added") or (cat == "Modded")):
                f = Files(fullPath, "L", SSH = ssh)
                f.transferFile(dest)

def makeLocalChanges(ssh):
    fullTxt = Settings().readSets()
    LocalDirectory = re.search('(?<=Local Directory: ).+', fullTxt).group()
    RemoteDirectory = re.search('(?<=Remote Directory: ).+', fullTxt).group()
    statsFile = Settings().readRem()
    if (statsFile == ""):
        Settings().rem.writeToFile(dict())
    oldStats = statsFile
    dataFile = Data(RemoteDirectory, "R", SSH = ssh)
    currentStats = dataFile.dict
    change = dataFile.compareChanges()
    for cat in change:
        for filename in change[cat]:
            fullPath = "%s/%s" % (RemoteDirectory, filename)
            dest = "%s/%s" % (LocalDirectory, filename)
            if ((cat == "Deleted") or (cat == "Modded")):
                if os.path.exists(dest):
                    if os.path.isdir(dest):
                        shutil.rmtree(dest)
                    else:
                        os.remove(dest)
            if ((cat == "Added") or (cat == "Modded")):
                f = Files(fullPath, "R", SSH = ssh)
                f.transferFile(dest)
            NowTime = datetime.datetime.now()
            s = "%s: %s/%s on %s:%s, %s/%s/%s" % (cat, LocalDirectory,
                                                    filename, str(NowTime.hour),
                                                    str(NowTime.minute),
                                                    str(NowTime.month),
                                                    str(NowTime.day),
                                                    str(NowTime.year))
            print s.encode("ascii", "ignore")

def updateR(ssh):
    fullTxt = Settings().readSets()
    LocalDirectory = re.search('(?<=Local Directory: ).+', fullTxt).group()
    RemoteDirectory = re.search('(?<=Remote Directory: ).+', fullTxt).group()
    remDataFile = Data(RemoteDirectory, "R", SSH = ssh)
    remDataFile.record()

def updateL(ssh):
    fullTxt = Settings().readSets()
    LocalDirectory = re.search('(?<=Local Directory: ).+', fullTxt).group()
    RemoteDirectory = re.search('(?<=Remote Directory: ).+', fullTxt).group()
    locDataFile = Data(LocalDirectory, "L", SSH = ssh)
    locDataFile.record()

def change_update_cycle(ssh):
    makeLocalChanges(ssh)
    makeRemoteChanges(ssh)
    updateL(ssh)
    updateR(ssh)