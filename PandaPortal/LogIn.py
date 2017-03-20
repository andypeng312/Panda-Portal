#!/usr/bin/env python

import paramiko
import os
from Files import *
from passwordPrompt import *
from ssh import *
from Settings import *

class LogIn(object):
    
    def __init__(self):
        login_ = promptPassword()
        if (login_ != None):
            (self.SSH, self.SFTP) = login_
        else:
            self.SSH = None
            self.SFTP = None
    
    def logout(self):
        self.SSH.close()