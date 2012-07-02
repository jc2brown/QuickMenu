#!/usr/bin/python

import sys
import subprocess
import settings



def print_menu(title, cmds, prev):
    print title
    for i in range(len(cmds)):
        print ' [' + str(i+1) + '] ' + cmds[i][0]
    print ' [0]', 'Exit' if len(prev) == 0 else 'Back'
        
        
def menu(title, lst, prevlst, input):
    
    cur = [(title, lst[:])]
    
    # I/O
    
    while True:
        print_menu(title, lst, prevlst)
        
        if input:
            choice = input[0]
            input = input[1:]
        else:            
            choice = raw_input()
            
        try:
            i = int(choice)
            if i >= 0 and i <= len(lst): break
        except ValueError:
            print "Enter a valid number"
    
    # Quit or back
    if i == 0:
        if len(prevlst) == 0:
            return 0
        else:
            title, lst = prevlst[0]
            return menu(title, lst, prevlst[1:], input)
    
        
    # Submenu or shell command
    i = i - 1   # Adjust from user input
    newtitle, cmd = lst[i]
    if type(cmd) is str:    # cmd is a shell command
        subprocess.call(cmd, shell=True)
        return menu(title, lst, prevlst, input)
    
    else:                    # cmd is a submenu
        return menu(newtitle, cmd, cur + prevlst, input)


menu('Home', settings.home_menu, [], sys.argv[1:])


