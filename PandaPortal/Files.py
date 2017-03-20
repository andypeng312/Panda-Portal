#!/usr/bin/env python

import os
import shutil
import paramiko
import sys

class Files(object):
    # creates object representing a file or folder
    SSH = None
    SFTP = None
    
    def __init__(self, path, location = "L", isFile = True, SSH = None):
        # creates file if it doesn't exist and stores it with name, location and
        # stats
        self.filename = path
        self.isFile = isFile
        self.location = location # "L" for local and "R" for remote
        (self.parentDirectory, self.baseFile) = os.path.split(self.filename)
        if ((SSH != None) and (Files.SSH == None) and
            (Files.SFTP == None)): # > 2 connections = crash
            Files.SSH = SSH
            Files.SFTP = SSH.open_sftp()
        self.create()
        self.isFile = Files.isfile(self.filename, self.location)
    
    def __repr__(self):
        return "Files('%s')" % (self.filename)
    
    def __eq__(self, other):
        return (self.filename == other.filename)
    
    ############################################################################
    def create(self):
        # create file if it doesn't exist
        if not Files.exists(self.filename, self.location):
            if (self.location == "L"):
                self.createL()
            elif(self.location == "R"):
                self.createR()
    ############################################################################
    
    def createL(self):
        # create file on local machine
        if not Files.exists(self.parentDirectory, "L"):
            self.createParentsL()
        if self.isFile:
            open(self.filename, "wb").close()
        else:
            os.mkdir(self.filename)
    
    def createParentsL(self, parent = None):
        # create parent folders
        if (parent == None):
            parent = self.parentDirectory
        (grandparentDirectory, parentBaseFile) = os.path.split(parent)
        if not Files.exists(grandparentDirectory, "L"):
            self.createParentsL(grandparentDirectory)
        os.mkdir(parent)
    
    def createR(self):
        # create remote file
        if not Files.exists(self.parentDirectory, "R"):
            self.createParentsR()
        if self.isFile:
            if not self.exists(self.filename, self.location):
                Files.SFTP.open(self.filename, "x").close()
        else:
            if not self.exists(self.filename, self.location):
                Files.SFTP.mkdir(self.filename)

    def createParentsR(self, parent = None):
        if (parent == None):
            parent = self.parentDirectory
        (grandparentDirectory, parentBaseFile) = os.path.split(parent)
        if not Files.exists(grandparentDirectory, "R"):
            self.createParentsR(grandparentDirectory)
        Files.SFTP.mkdir(parent)
    
    ############################################################################
    @classmethod
    def exists(cls, path, location):
        if (location == "L"):
            return os.path.exists(path)
        elif (location == "R"):
            try:
                if (os.path.basename(path) in
                    Files.SFTP.listdir(os.path.dirname(path))):
                    # if file exists in the specified directory
                    return True
                else:
                    return False
            except IOError as error:
                if ((error.errno == 2) and (error.strerror == "No such file")):
                    return False
                else:
                    raise
    ############################################################################
    
    ############################################################################
    @classmethod
    def isfile(cls, path, location):
        if Files.exists(path, location):
            if (location == "L"):
                return os.path.isfile(path)
            elif (location == "R"):
                try:
                    Files.SFTP.open(path, "r").read()
                    return True
                except IOError as error:
                    if (error.message == "Failure"):
                        return False
                    else:
                        raise
        else:
            return False
    ############################################################################
    
    ############################################################################
    def relpath(self, directory):
        direc = directory
        path = self.filename
        splitRelPath = []
        while (direc in os.path.dirname(path)):
            splitRelPath.append(os.path.basename(path))
            path = os.path.dirname(path)
        return "/".join(reversed(splitRelPath))
    ############################################################################
    
    ############################################################################
    def fileStats(self):
        if (self.location == "L"):
            return os.stat(self.filename)
        elif (self.location == "R"):
            return Files.SFTP.stat(self.filename)
    ############################################################################
    
    ############################################################################
    def writeToFile(self, data, append = False):
        if append:
            mode = "ab" # write, append, binary mode
        else:
            mode = "wb" # write, binary mode
        if (type(data) != str): # if data is not of string type
            data = "**REPR**" + repr(data) # mark data
        if (self.location == "L"):
            f = open(self.filename, mode)
        elif (self.location == "R"):
            f = Files.SFTP.open(self.filename, mode)
        f.write(data)
        f.close()
    ############################################################################
    
    ############################################################################
    def readFromFile(self): # reads data from file
        mode = "rb"
        if (self.location == "L"):
            if self.isFile:
                f = open(self.filename, mode)
            else:
                return None
        elif (self.location == "R"):
                f = Files.SFTP.open(self.filename, mode)
        try:
            if (f.read(8) == "**REPR**"): # reads in 8 lines
                data = eval(f.read())
            else:
                f.seek(0) # if first 8 lines are not **REPR**, goes to beginning
                data = f.read()
        except IOError as error:
            if (error.message == "Failure"): # remote file is a folder
                data = None
            else:
                raise
        f.close()
        return data
    ############################################################################
    
    ############################################################################
    def delete(self):
        if (self.location == "L"):
            if self.isFile:
                os.remove(self.filename)
            else:
                shutil.rmtree(self.filename)
        elif (self.location == "R"):
            if self.isFile:
                Files.SFTP.remove(self.filename)
            else:
                Files.rmtreeR(self.filename)
    ############################################################################
    
    @classmethod
    def rmtreeR(cls, filename):
        if Files.isfile(filename, "R"):
            Files.SFTP.remove(filename)
        elif (len(Files.SFTP.listdir(filename)) == 0):
            Files.SFTP.rmdir(filename)
        else:
            for subFile in Files.SFTP.listdir(filename):
                fullPath = "%s/%s" % (filename, subFile)
                Files.rmtreeR(fullPath)
            Files.SFTP.rmdir(filename)
    
    ############################################################################
    def transferFile(self, destination):
        # download or upload
        if (self.location == "L"):
            self.upload(destination)
        if (self.location == "R"):
            self.download(destination)
        if "IamErrorFearMe" in self.filename:
            raise
    ############################################################################
    
    def upload(self, destination):
        try:
            Files.SFTP.put(self.filename, destination) # will overwrite
                                                        # existing file
        except IOError as error:
            if ((error.errno == 2) and (error.strerror == "No such file")):
                parentDir = os.path.dirname(destination)
                Files(parentDir, "R", False, Files.SSH)
                Files.SFTP.put(self.filename, destination)
            elif ((error.errno == 21) and
                (error.strerror == "Is a directory")):
                Files(destination, "R", False, Files.SSH)
            else:
                raise
    
    def download(self, destination):
        parentDir = os.path.dirname(destination)
        if not Files.exists(parentDir, "L"):
            Files(parentDir, "L", False, Files.SSH)
        if Files.isfile(self.filename, "R"):
            Files.SFTP.get(self.filename, destination)
        else:
            if not Files.exists(destination, "L"):
                os.mkdir(destination)
    
    ############################################################################
    @classmethod
    def getFileContentData(cls, path, location, isFile = False, SSH = None):
        fileList = set()
        if (location == "L"):
            if os.path.isdir(path):
                for subFile in os.listdir(path):
                    subPath = path + "/" + subFile
                    subIsFile = os.path.isfile(subPath)
                    fileList = fileList | (cls.getFileContentData(subPath,
                                                                  "L",
                                                                  subIsFile,
                                                                  SSH))
            fileList.add(Files(path, "L", isFile, SSH))
        elif (location == "R"):
            try:
                for subFile in SSH.open_sftp().listdir(path):
                    subPath = path + "/" + subFile
                    fileList = fileList | (cls.getFileContentData(subPath,
                                                                  "R",
                                                                  SSH = SSH))
                fileList.add(Files(path, location, False, SSH))
            except IOError as error:
                if ((error.errno == 2) and (error.strerror == "No such file")):
                    fileList.add(Files(path, "R", True, SSH))
                else:
                    raise
        return fileList
    ############################################################################