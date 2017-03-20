#!/usr/bin/env python

from Files import *
from UnexpectedErrors import *
import Tkinter
import tkFileDialog
import os

def initSettingsText(root, settings):
    settings.serverCat = "Server: "
    settings.serverCatRow = 1
    settings.localDirCat = "Local Directory: "
    settings.localDirRow = 3
    settings.remoteDirCat = "Remote Directory: "
    settings.remoteDirRow = 5
    makeGUIvars(root, settings)
    return settings

def makeGUIvars(root, settings):
    settings.labelCol = 1
    settings.entCol = 2
    settings.entColSpan = 3
    settings.entWid = 40
    settings.locdirtxt = Tkinter.StringVar(root)
    settings.remdirtxt = Tkinter.StringVar(root)
    return settings

#######################################
def loadSettings():
    root = Tkinter.Tk()
    root.title("Preferences")
    root.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
    class Struct: pass
    settings = Struct()
    initSettingsText(root, settings)
    drawUserInput1(root, settings)
    root.mainloop()
#######################################

def drawUserInput1(root, settings):
    drawGetServer(root, settings)
    drawGetLocalDir(root, settings)
    drawGetRemoteDir(root, settings)
    drawGetUpdateFrequency(root, settings)

def drawGetServer(root, settings):
    Lbllocation = (settings.serverCatRow, settings.labelCol)
    sLbl1 = makeLabel(root, Lbllocation, text = settings.serverCat)
    EntLocation = (settings.serverCatRow, settings.entCol,
                   settings.entColSpan)
    settings.Sentry = makeEntry(root, EntLocation, width = settings.entWid)
    sLbl2 = Tkinter.Label(root)
    sLbl2.grid(row = settings.serverCatRow + 1, column = settings.labelCol)

def drawGetLocalDir(root, settings):
    Lbllocation = (settings.localDirRow, settings.labelCol)
    locLbl1 = makeLabel(root, Lbllocation, text = settings.localDirCat)
    EntLocation = (settings.localDirRow, settings.entCol + 1,
                   settings.entColSpan - 1)
    settings.Lentry = makeEntry(root, EntLocation, width = 4*settings.entWid/5,
              textvariable = settings.locdirtxt)
    ButtLocation = settings.localDirRow, settings.labelCol + 1
    command = lambda: pickFile(settings, "loc")
    locBut = makeButton(root, ButtLocation, text = "Pick", command = command)
    locLbl2 = Tkinter.Label(root)
    locLbl2.grid(row = settings.serverCatRow + 3, column = settings.labelCol)

def drawGetRemoteDir(root, settings):
    Lbllocation = (settings.remoteDirRow, settings.labelCol)
    remLbl1 = makeLabel(root, Lbllocation, text = settings.remoteDirCat)
    EntLocation = (settings.remoteDirRow, settings.entCol + 1,
                   settings.entColSpan - 1)
    settings.Rentry = makeEntry(root, EntLocation, width = 4*settings.entWid/5,
              textvariable = settings.remdirtxt)
    ButtLocation = settings.remoteDirRow, settings.labelCol + 1
    command = lambda: pickFile(settings, "rem")
    remBut = makeButton(root, ButtLocation, text = "Pick", command = command)
    makeButtons(root, settings)
    remLbl2 = Tkinter.Label(root)
    remLbl2.grid(row = settings.serverCatRow + 5, column = settings.labelCol)

def drawGetUpdateFrequency(root, settings):
    Lbllocation = (settings.remoteDirRow + 5, settings.labelCol)
    upLbl1 = makeLabel(root, Lbllocation,
                       text = "Update Frequency (Per 10 minutes)")
    sliderLocation = (settings.remoteDirRow + 3, settings.entCol,
                   settings.entColSpan)
    settings.slid = makeSlider(root, sliderLocation, from_ = 1, to = 120,
                               orient = Tkinter.HORIZONTAL, length = 300)
    upLbl2 = Tkinter.Label(root)
    upLbl2.grid(row = settings.serverCatRow + 12, column = settings.labelCol)

def makeLabel(root, location, **Options):
    (row_, col) = location[0], location[1]
    Lbl = Tkinter.Label(root, **Options)
    if len(location) > 2:
        colspan = location[2]
        Lbl.grid(row = row_, column = col, columnspan = colspan)
    else:
        Lbl.grid(row = row_, column = col)
    return Lbl

def makeEntry(root, location, **Options):
    field = Tkinter.Entry(root, **Options)
    (row_, col) = location[0], location[1]
    Ent = Tkinter.Entry(root, **Options)
    if len(location) > 2:
        colspan = location[2]
        Ent.grid(row = row_, column = col, columnspan = colspan)
    else:
        field.grid(row = row_, column = col)
    return Ent

def makeButton(root, location, **Options):
    (row_, col) = location[0], location[1]
    B= Tkinter.Button(root, **Options)
    (row_, col) = location[0], location[1]
    B.grid(row = row_, column = col)
    return B

def makeSlider(root, location, **Options):
    slid = Tkinter.Scale(root, **Options)
    (row_, col) = location[0], location[1]
    slid = Tkinter.Scale(root, **Options)
    if len(location) > 2:
        colspan = location[2]
        slid.grid(row = row_, column = col, columnspan = colspan, rowspan = 3)
    else:
        slid.grid(row = row_, column = col)
    return slid

def pickFile(settings, x):
    filen = tkFileDialog.askdirectory(title = "Please choose a directory")
    if x == "rem":
        settings.remdirtxt.set(filen)
    elif x == "loc":
        settings.locdirtxt.set(filen)

def makeButtons(root, settings):
    save = lambda: saveSets(root, settings)
    settings.button = Tkinter.Button(root, text = "Save", command = save)
    settings.button.grid(row = 14, column = 2)
    end = lambda: root.destroy()
    settings.cancel = Tkinter.Button(root, text = "Cancel", command = end)
    settings.cancel.grid(row = 14, column = 3)

def saveSets(root, settings):
    data = ("Server: %s\nLocal Directory: %s\nRemote Directory: %s\nUpdate Frequency: %s"
            % (settings.Sentry.get(), settings.Lentry.get(),
               settings.Rentry.get(), settings.slid.get()))
    f = Files(os.path.abspath(".config/settings"))
    f.writeToFile(data)
    ErrorClass.LoadLocalDir
    root.destroy()