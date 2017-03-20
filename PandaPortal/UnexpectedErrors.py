#!/usr/bin/env python
# handles uncaught exceptions, sys.stderr is redirected through ErrorClass
# object
import subprocess
import shutil
import os
import time
import Tkinter
import string
from MakeChanges import *
from runinbg import *

class ErrorClass(object):
    Errors = 0
    LocalDirectory = None
    errorLog = "ErrorMessage.txt"
    def __init__(self):
        open(ErrorClass.errorLog, "wb").close() #creates file or resets it
        ErrorClass.LoadLocalDir()
    
    def write(self, errormsg): # redefines the procedure of returning an error
                               # message
        if (ErrorClass.LocalDirectory != None): #backup
            if not os.path.exists("RecoveredFiles"):
                times = time.time()
                Bfilename = "RecoveredFiles%d" % times
                if not os.path.exists(Bfilename):
                    shutil.copytree(ErrorClass.LocalDirectory, Bfilename)
        f = open(ErrorClass.errorLog, "ab")
        f.write(errormsg)
        f.close()
        ErrorClass.Errors += 1
    
    @classmethod
    def LoadLocalDir(cls):
        fullTxt = Settings().readSets()
        if (re.search('(?<=Local Directory: ).+', fullTxt) != None):
                ErrorClass.LocalDirectory = re.search('(?<=Local Directory: ).+',
                                           fullTxt).group()

class ErrorWindow(object):
    textLines = 0
    text = []
    canWid = 1000
    def __init__(self):
        time.sleep(10)
        f = open(ErrorClass.errorLog, "rb")
        Errortext = f.read()
        f.close()
        while not (lettersInText(Errortext)):
            f = open(ErrorClass.errorLog, "rb")
            Errortext = f.read()
            f.close()
        self.root = Tkinter.Tk()
        self.root.wm_attributes("-topmost", 1)
        self.root.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
        self.root.title("Panda Portal encountered an error...")
        self.canvas = Tkinter.Canvas(self.root,
                                     height = (20 * ErrorWindow.textLines),
                                     width = ErrorWindow.canWid)
        self.canvas.pack()
        self.Timer()
        self.root.mainloop()
    
    def Timer(self):
        f = open(ErrorClass.errorLog, "rb")
        ErrorWindow.text = f.read().split("\n")
        ErrorWindow.textLines = len(ErrorWindow.text)
        self.redrawAll()
        self.canvas.after(1000, self.Timer)
    
    def redrawAll(self):
        self.canvas.delete(Tkinter.ALL)
        self.canvas.config(height = 20 * ErrorWindow.textLines)
        for line in xrange(ErrorWindow.textLines):
            color = "gray" if ((line % 2) == 0) else "white"
            pt1 = (0, (20 * line))
            pt2 = (ErrorWindow.canWid, (20 * (line + 1)))
            self.canvas.create_rectangle(pt1, pt2, fill = color, width = 0)
            self.canvas.create_text(10, (20 * (line + 0.5)),
                                    text = ErrorWindow.text[line], anchor = "w",
                                    font = ("courier", 12), fill = "red")

def lettersInText(s):
    for char in (string.ascii_letters + string.digits):
        if char in s:
            return True
    return False

#os.chdir(os.path.dirname(sys.argv[0]))
#ErrorWindow()