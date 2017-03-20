#password prompt with Tkinter

import Tkinter
from ssh import *
from Files import *
import re
import time

##### function of interest, starts log-in dialog and returns sshSession object
def promptPassword(loginConfig = ".config/login",
                   settingsFile = ".config/settings"):
    settings = Files(os.path.abspath(settingsFile))
    fullTxt = settings.readFromFile()
    server = re.search('(?<=Server: ).+', fullTxt).group()
    class Struct: pass
    vars = Struct()
    vars.server = server
    root = start()
    vars = initVars(vars, root)
    draw(vars, root)
    comm = lambda x: keyPressed(x, vars, root)
    root.bind("<Return>", comm)
    root.mainloop()
    return vars.sshSession

######

def start():
    root = Tkinter.Tk()
    root.title("Login")
    root.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
    return root

####init variables
def initVars(vars, root):
    vars = initStatVars(vars)
    vars = initDynVars(root, vars)
    return vars
    

def initStatVars(vars):
    vars = initButtonInfo(vars)
    vars = initFldInfo(vars)
    vars = initEmpyLblInfo(vars)
    vars = initCheckButtonInfo(vars)
    return vars

def initEmpyLblInfo(vars):
    vars.emptyLblWid = 10
    vars.emptyLblRow = 3
    vars.emptyLblCol = 3
    return vars

def initButtonInfo(vars):
    vars.buttonRow = 4
    vars.connectTxt = "Connect"
    vars.connectCol = 1
    vars.cancelTxt = "Cancel"
    vars.cancelCol = 2
    return vars

def initFldInfo(vars):
    vars.usrTxt = "Username"
    vars.pwTxt = "Password"
    vars.usrRow = 0
    vars.pwRow = 1
    vars.lblWid = 10
    vars.entWid = 30
    vars.entCol = 1
    vars.entColSpan = 3
    return vars

def initCheckButtonInfo(vars):
    vars.checkButtonRow = 2
    vars.checkButtonCol = 1
    vars.checkButtonColSpan = 2
    vars.checkButtonTxt = "Remember me"
    vars.checked = False
    return vars

def initDynVars(root, vars):
    vars.connectInfo = {"user": "", "pw": ""}
    vars.connectingTxt = Tkinter.StringVar(root)
    vars.connectingWid = 20
    vars.connectingRow = 3
    vars.connectingCol = 1
    vars.connectingColSpan = 2
    vars.connecting = False
    vars.connected = False
    vars.sshSession = None
    return vars
######

###### draw widgets
def draw(vars, root):
    vars.user = makeField(root, vars.usrTxt, vars.usrRow, vars.lblWid,
                          vars.entWid, vars.entCol, vars.entColSpan)
    vars.pw = makeField(root, vars.pwTxt, vars.pwRow, vars.lblWid, vars.entWid,
                     vars.entCol, vars.entColSpan, show = "*")
    connectComm = lambda: getUserPW(vars, root)
    cancelComm = lambda: kill(root)
    connection = makeButton(root, vars.connectTxt, vars.connectCol,
                         connectComm, vars.buttonRow)
    cancel = makeButton(root, vars.cancelTxt, vars.cancelCol, cancelComm,
                        vars.buttonRow)
    checkButtonComm = lambda: checkButton(vars)
    Tkinter.Checkbutton(root, text = vars.checkButtonTxt, command = checkButtonComm
                ).grid(row = vars.checkButtonRow, column = vars.checkButtonCol,
                       columnspan = vars.checkButtonColSpan)
    #acts as a spacer to keep window correct size
    Tkinter.Label(root, width = vars.emptyLblWid).grid(row = vars.emptyLblRow,
                                               column = vars.emptyLblCol)
    #holds space for text later
    txtLbl = Tkinter.Label(root, textvariable = vars.connectingTxt, width =
                   vars.connectingWid)
    txtLbl.grid(row = vars.connectingRow, column = vars.connectingCol,
                columnspan = vars.connectingColSpan)

def makeField(root, txt, rownumber, lblWid, entWid, entCol, entColSpan,
              **options):
    Lbl = Tkinter.Label(root, text=txt, width = lblWid)
    Lbl.grid(row = rownumber)
    field = Tkinter.Entry(root, width = entWid, **options)
    field.grid(row = rownumber, column = entCol, columnspan = entColSpan)
    return field

def makeButton(root, txt, columnnumber, comm, buttonRow, **options):
    button = Tkinter.Button(root, text = txt, command = comm, **options)
    button.grid(row = buttonRow, column = columnnumber)
    return button
    
##### draw widgets

##### actions
def getUserPW(vars, root):
    getUserPW_helper1(vars, root)
    getUserPW_helper2(vars, root)

def getUserPW_helper1(vars, root):
    userEntry = vars.user.get()
    pwEntry = vars.pw.get()
    vars.connectInfo = {"user": userEntry, "pw": pwEntry}
    vars.connecting = True

def getUserPW_helper2(vars, root):
    makeConnection(root, vars)
    if vars.connected:
        time.sleep(1)
        root.destroy()

def makeConnection(root, vars):
    vars.connectingTxt.set("Connecting to server...")
    root.update_idletasks()
    try:
        vars.sshSession = login(vars.connectInfo["user"],
                                vars.connectInfo["pw"], vars.server)
        vars.connected = True
        if (vars.checked == True):
            storeKeyChain(vars.connectInfo)
            makeConfigFile(vars.connectInfo["user"])
        vars.connectingTxt.set("Connected, enjoy!")
        root.update_idletasks()
    except Exception as error:
        if isinstance(error, paramiko.AuthenticationException):
            vars.connected = False
            vars.pw.delete(0, Tkinter.END)
            vars.connectingTxt.set("Authentication failed")
            root.update_idletasks()
        else:
            raise

def checkButton(vars):
    vars.checked = not vars.checked

def keyPressed(event, vars, root):
    getUserPW(vars, root)

def kill(root):
    root.destroy()