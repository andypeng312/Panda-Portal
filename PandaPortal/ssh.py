#!/usr/bin/env python

import paramiko
import subprocess
import re
import shlex
from Files import *

def login(user, pw, server): # need to hold onto ssh variable to work!
    ssh = paramiko.SSHClient() #opens ssh connection
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username = user, password = pw)
    sftpSession = ssh.open_sftp()
    return ssh, sftpSession

def makeConfigFile(user, loginConfig = ".config/login"):
    txt = "#saved login \nUser: %s" % (user)
    f = Files(loginConfig)
    f.writeToFile(txt)

def storeKeyChain(loginInfo, server = None, settingsFile = ".config/settings"):
    if (server == None):
        settings = Files(settingsFile)
        fullTxt = settings.readFromFile()
        server = re.search('(?<=Server: ).+', fullTxt).group()
    usr = loginInfo["user"]
    pw = loginInfo["pw"]
    command = shlex.split("security  add-internet-password -a %s -s %s -w %s -U"
               % (repr(usr), repr(server), repr(pw)))
    subprocess.Popen(command, shell = False)

def retrieveKeyChain(configFile = ".config/login",
                     server = None, settingsFile = ".config/settings"):
    if not os.path.exists(configFile):
        return {"user": "", "pw": ""}
    if (server == None):
        settings = Files(settingsFile)
        fullTxt = settings.readFromFile()
        server = re.search('(?<=Server: ).+', fullTxt)
        if (server != None):
            server = server.group()
        else:
            server = ""
    cFile = Files(configFile)
    fullTxt = cFile.readFromFile()
    usr = re.search('(?<=User: ).+', fullTxt)
    if (usr != None):
        usr = usr.group()
    else:
        usr = ""
    command = shlex.split("security  find-internet-password -ga %s -s %s" %
                          (repr(usr), repr(server)))
    rawTxt = subprocess.Popen(command, shell = False,
                              stderr = subprocess.PIPE,
                              stdout = subprocess.PIPE,
                              stdin = subprocess.PIPE).stderr.read()
    pw = re.search('(?<=password: ").+', rawTxt)
    if (pw != None):
        pw = pw.group()
        pw = pw[0: (len(pw) - 1)]
    else:
        pw = ""
    return {"user": usr, "pw": pw}