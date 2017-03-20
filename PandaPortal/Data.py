#!/usr/bin/env python

from Files import *
import os
import time

class Data(Files):

    def __init__(self, directory, location, SSH = None):
        done = False
        while (done == False):
            try:
                Files.__init__(self, directory, location, False, SSH)
                self.SSH = SSH
                self.fileList = Files.getFileContentData(directory, location, False, SSH)
                self.dict = {fileobj.relpath(self.filename):fileobj.fileStats().st_mtime
                                 for fileobj in self.fileList if fileobj.filename !=
                                 self.filename}
                done = True
            except IOError as error:
                if ((error.errno == 2) and (error.strerror == "No such file")):
                    time.sleep(5) #files are probably being modified
                else:
                    raise
    
    def record(self):
        if (self.location == "L"):
            f = Files(os.path.abspath(".config/LocalFiles"))
        elif (self.location == "R"):
            f = Files(os.path.abspath(".config/RemoteFiles"))
        f.writeToFile(self.dict)
    
    def compareChanges(self):
        if (self.location == "L"):
            locale = "L"
            f = Files(".config/LocalFiles")
            oldStats = f.readFromFile()
        elif (self.location == "R"):
            locale = "R"
            f = Files(".config/RemoteFiles")
            oldStats = f.readFromFile()
        currentStats = self.dict
        changed = dict()
        changed["Deleted"] = set(oldStats.keys()) - set(currentStats.keys())
        changed["Added"] = set(currentStats.keys()) - set(oldStats.keys())
        union = (set(currentStats.keys()) & set(oldStats.keys()))
        changed["Modded"] = set()
        for key in union:
            if (currentStats[key] > oldStats[key]):
                fullPath = self.filename + "/" + key
                f = Files(fullPath, self.location, self.SSH)
                if Files.isfile(f.filename, locale):
                    changed["Modded"].add(key)
        return changed