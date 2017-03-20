#!/usr/bin/env python
import os
import Tkinter
import sys
from LogIn import *
from Settings import *
from MakeChanges import *
from RunApp import *

def mousePressed(event):
    mousePosition(event)
    if (canvas.MouseLocation == "Button1"):
        canvas.buttonBorder1 += 2
    elif (canvas.MouseLocation == "Button2"):
        canvas.buttonBorder2 += 2
    elif (canvas.MouseLocation == "Button3"):
        canvas.buttonBorder3 += 2
    redrawAll()

def mouseReleased(event, root):
    canvas.buttonBorder1 = 2
    canvas.buttonBorder2 = 2
    canvas.buttonBorder3 = 2
    if (canvas.MouseLocation == "Button1"):
        if (canvas.warningText == 1):
            canvas.warningText = 0
        settings = Files(os.path.abspath(".config/settings"))
        fullTxt = settings.readFromFile()
        server = re.search('(?<=Server: ).+', fullTxt)
        if (server != None):
            server = server.group()
            loginConfig = ".config/login"
            if os.path.exists(loginConfig):
                sshSession = autoLogin(loginConfig, server)
                if (sshSession != None):
                    canvas.login = sshSession
            else:
                loginDialog()
        else:
            canvas.warningText = 2
    elif (canvas.MouseLocation == "Button2"):
        if (canvas.warningText == 2):
            canvas.warningText = 0
        loadSettings()
    elif (canvas.MouseLocation == "Button3"):
        if (canvas.login != None):
            canvas.end = True
            root.destroy()
            startRunning(canvas.login)
        else:
            canvas.warningText = 1

def loginDialog():
    canvas.end = True
    login = LogIn()
    run(login)

def startRunning(login):
    login = canvas.login
    fullTxt = Settings().readSets()
    timesPer10Minutes = re.search('(?<=Update Frequency: ).+', fullTxt).group()
    main(login, int(timesPer10Minutes))
    
def mousePosition(event):
    if (canvas.buttonx1 < event.x < canvas.buttonx2):
        if (canvas.button1 < event.y < canvas.button1 + canvas.buttonh):
            canvas.MouseLocation = "Button1"
        elif (canvas.button2 < event.y < canvas.button2 + canvas.buttonh):
            canvas.MouseLocation = "Button2"
        elif (canvas.button3 < event.y < canvas.button3 + canvas.buttonh):
            canvas.MouseLocation = "Button3"
        else:
            canvas.MouseLocation = None
    else:
        canvas.MouseLocation = None

def timerFired(root):
    if (canvas.end == False):
        redrawAll()
        delay = 500 # milliseconds
        canvas.after(delay, timerFired, root) #pause, then call timerFired again
    else:
        root.destroy()

def redrawAll():
    canvas.delete(Tkinter.ALL)
    DrawPanda()
    DrawTxt()
    DrawButtons()
    if (canvas.warningText == 1):
        canvas.create_text(250, 150, text = "Please Log In", fill = "red")
    elif (canvas.warningText == 2):
        canvas.create_text(250, 150, text = "Check Your Settings",
                           fill = "red")
    if (canvas.login != None):
        canvas.warningText = 0
        canvas.create_text(250, 150, text = "Logged in, you may proceed",
                           fill = "blue")

def DrawTxt():
    canvas.create_text(325, 82, text = canvas.MainScreenTxt1,
                       font = canvas.Font, anchor = "se", fill = "blue")
    canvas.create_text(275, 62, text = canvas.MainScreenTxt2,
                       font = canvas.Font, anchor = "nw", fill = "blue")

def DrawButtons():
    button1coords = (canvas.buttonx1, canvas.button1, canvas.buttonx2,
                     canvas.button1 + canvas.buttonh)
    canvas.create_rectangle(button1coords, fill = "gray",
                            width = canvas.buttonBorder1)
    canvas.create_text(canvas.textx, canvas.text1y, text = "Login")
    button2coords = (canvas.buttonx1, canvas.button2, canvas.buttonx2,
                     canvas.button2 + canvas.buttonh)
    canvas.create_rectangle(button2coords, fill = "gray",
                            width = canvas.buttonBorder2)
    canvas.create_text(canvas.textx, canvas.text2y, text = "Settings")
    button3coords = (canvas.buttonx1, canvas.button3, canvas.buttonx2,
                     canvas.button3 + canvas.buttonh)
    canvas.create_rectangle(button3coords, fill = "gray",
                            width = canvas.buttonBorder3)
    canvas.create_text(canvas.textx, canvas.text3y, text = "Start!")

def DrawPanda():
    canvas.create_rectangle(canvas.boxCoords, fill = "cyan", width = 2)
    canvas.create_image(100, 90, image = canvas.Panda)

def init():
    canvas.MainScreenTxt1 = "Panda"
    canvas.MainScreenTxt2 = "Portal!"
    canvas.Font = ("Bookman", 55, "bold")
    canvas.Panda = Tkinter.PhotoImage(file = "Panda.gif")
    canvas.boxCoords = (5, 25, 500, 120)
    canvas.buttonx1 = 200
    canvas.buttonx2 = 300
    canvas.buttonh = 20
    canvas.textx = 250
    canvas.button1 = 180
    canvas.text1y = 190
    canvas.button2 = 210
    canvas.text2y = 220
    canvas.button3 = 240
    canvas.text3y = 250
    canvas.buttonBorder1 = 2
    canvas.buttonBorder2 = 2
    canvas.buttonBorder3 = 2
    canvas.MousePressed = False
    canvas.MouseLocation = None
    canvas.end = False
    canvas.login = None
    canvas.warningText = 0

def autoLogin(loginConfig, server = "unix.andrew.cmu.edu"):
    loginInfo = retrieveKeyChain(loginConfig)
    try:
        class Struct(): pass
        sshSession = Struct()
        (sshSession.SSH, sshSession.SFTP) = login(loginInfo["user"],
                                                  loginInfo["pw"], server)
        return sshSession
    except Exception as error:
        if isinstance(error, paramiko.AuthenticationException):
            os.remove(loginConfig)
            loginDialog()
        else:
            raise

def run(login = None):
    # create the root and the canvas
    root = Tkinter.Tk()
    global canvas
    root.title("Welcome to Panda Portal!")
    canvas = Tkinter.Canvas(root, width=500, height=300)
    root.resizable(width=Tkinter.FALSE, height=Tkinter.FALSE)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    init()
    if ((login != None) and (login.SSH != None) and (login.SFTP != None)):
        canvas.login = login
    # set up events
    mouse = lambda x: mouseReleased(x, root)
    root.bind("<Button-1>", mousePressed)
    root.bind("<ButtonRelease-1>", mouse)
    timerFired(root)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close
                     # the window!)