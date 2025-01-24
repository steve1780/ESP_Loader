#!/usr/bin/env python

''' ESP Loader 0.1

1-22-25     s.case      ESP32 program loader
                        Handheld device that can upload micropython programs on a target
                        connected by USB.

                        Will be hosted on Raspberry Pi and will execute mpfshell commands
                        3.5" Touch screen for user input

                        Working. Proof of concept successful.
                        
1-24-25                 version 0.1 ok, mpf commands working
'''

#import RPi.GPIO as GPIO
import os
import sys
from time import sleep
# import paho.mqtt.client as mqtt

### TODO Select port ESP is connected to
COMPORT = "ttyUSB0"
flist = []

def flushport(port):
    os.system('stty -F /dev/' + port + ' -hupcl')  # do this the hard way vs changing mfpshell
    print('stty -F /dev/' + port + ' -hupcl')    

def mpf_reset(port):
    os.system('mpfshell -n -c ' + '"open ' + port + '; --reset ' + '" > reset.txt')

def filelist():
    global flist
    with open("out.txt", "r") as file:
        flist = file.readlines()
    # Remove \n characters from each line
    flist = [line.strip() for line in flist]
    for line in range(0,4) :
        flist.pop(0)  # these messages are not necessary for the file list
    flist.pop(-1)     # cr at the end of the listing, remove it
    file.close()      # be nice!

def mpf_ls(port):
    # mpfshell ls command ====================================================================
    os.system('mpfshell -n -c ' + '"open ' + port + '; ls ' + '" > out.txt')
    filelist()
    print("Programs on target: ")
    print(flist)
    flushport(port)

def mpf_lls(port):
    # mpfshell lls command ====================================================================
    os.system('mpfshell -n -c ' + '"open ' + port + '; lls ' + '" > out.txt')
    filelist()
    print("Programs on tool: ")
    print(flist) 
    flushport(port)

def mpf_rm(port, fname):
    # mpfshell rm command ====================================================================
    # file will come from selecting one of the targets programs
    ### TODO will need ok, cancel

    os.system('mpfshell -n -c ' + '"open ' + port + '; rm ' + fname + '" > rmout.txt')
    print("Programs ", fname, " deleted from target ")
    flushport(port)


def mpf_put(port, fname):
    # mpfshell put command ====================================================================
    ### TODO file check
    # mpfshell ls
    # see if fname file is in resulting list
    #   if so issue warning and get user response, to copy over target?
    
    os.system('mpfshell -n -c ' + '"open ' + port + '; put ' + fname + '" > putout.txt')    
    print("Programs ", fname, " copied to target ")
    flushport(port)



flushport(COMPORT)           # do this upon re-connecting the target  
mpf_ls(COMPORT)   
mpf_rm(COMPORT, "test")
mpf_ls(COMPORT) 
mpf_put(COMPORT, "test")
mpf_ls(COMPORT)   
# mpf_reset(COMPORT)         # seems to work ok, not sure if/when will be needed
