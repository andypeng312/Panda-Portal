# README
## Description of Project
I wrote this program when I was first learning Python. The project is a program
that syncs files and folders between two directories, one local to the user's
computer and one on a remote server. At the time, I used it to sync files 
between my personal computer and my university's servers.

The interface allows you to log into any remote server and select a local and
remote directory to sync up as well as the rate at which the program checks for
changes. Once started, the program runs silently in the background and will
remember these settings the next time it starts. While running, the program 
also keeps a log of which files are created, deleted, or modified as well as a 
record of any errors that occur.

The entire program is written in Python using the following built in modules:
* os
* time
* shutil
* sys
* resource
* re
* datetime
* Tkinter
* tkFileDialog, 
* subprocess
* shlex
* string  
I used one third-party module called Paramiko to transfer files and make
changes to the remote directory using SSH. Finally, I bundled all of the
actions and shell scripts needed to start the Python scripts into an Automator
workflow on Mac OS so that it can be started by clicking a single icon on the
desktop.

## Contents
* **`PandaPortal` (folder)**- contains the files and code for the project
* **`PandaPortal` (application)**- Automator app that runs the program
* **`screen_recording.mp4`**- a screen recording of the program
* **`screenshots`**- contains images of the program
---

**Technologies:** Python, Shell scripting, SSH, Automator workflows, 
Regular expressions, File I/O, GUI, Exception handling  
**Estimated Lines of Code:** 1200

![](/screenshots/screenshot1.png)

![](/screenshots/screenshot2.png)