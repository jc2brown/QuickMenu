#!/usr/bin/python

import sys
import subprocess

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



system_menu = [
               ('Bounce', 'sudo reboot'),
               ('Down', 'sudo shutdown -P now')
               ]


tomcat7_menu = [
                ('Bounce', 'sudo /usr/share/tomcat7/bin/shutdown.sh; sudo /usr/share/tomcat7/bin/startup.sh'),
                ('Down', 'sudo /usr/share/tomcat7/bin/shutdown.sh'),
                ('Up', 'sudo /usr/share/tomcat7/bin/startup.sh')
                ]


apache2_menu = [
                ('Bounce', 'sudo /etc/init.d/apache2 restart'),
                ('Down', 'sudo /etc/init.d/apache2 stop'),
                ('Up', 'sudo /etc/init.d/apache2 start'),
                ('Edit', 'sudo nano /etc/apache2/sites-enabled/000-default')
                ]


# Be careful here, these directories will be mirrored to the cloud server
rsync_dirs = [
              '/test',
              '/test2',
              '/etc/apache2/',
              '/var/www/jc2brown.ca',
              '/var/www/toeachtheirown.net'
              ]

teto_dirs = [
              '/var/www/toeachtheirown.net'
              ]




HQToCloud_cmd = ''
for dir in rsync_dirs:
    HQToCloud_cmd += 'rsync -RrPvaz --delete --rsh "ssh -i /home/chris/jc2brown_key.pem" --rsync-path "rsync" ' + dir + ' ubuntu@jc2brown.ca:/; '

TetoToCloud_cmd = ''
for dir in teto_dirs:
    TetoToCloud_cmd +=  'rsync -RrPvaz --delete --rsh "ssh -i /home/chris/jc2brown_key.pem" --rsync-path "rsync" ' + dir + ' ubuntu@jc2brown.ca:/; '



cloud_menu = [
             ('Push to Cloud', HQToCloud_cmd),
             ('TETO to Cloud', TetoToCloud_cmd),
             ('ssh jc2brown.ca', 'ssh -i /home/chris/jc2brown_key.pem ubuntu@jc2brown.ca')
             ]


# Replace current version with latest copy from repo
selfupdate_cmd = '''
    svn co svn://jc2brown.ca/svn/QuickMenu/trunk/src;
    mv -f src/menu.py /usr/bin/menu;
    chmod +x /usr/bin/menu; 
    rm -rf src;
'''


home_menu = [
             ('System', system_menu),
             ('Apache2', apache2_menu),
             ('Tomcat7', tomcat7_menu),
             ('Cloud', cloud_menu),
             ('Self-Update', selfupdate_cmd)
             ]


''' Grammar for a menu

menu : list(item)
item: tuple(title, action)
title: string
action: menu | shellcommand
shellcommand: string
'''


menu('Home', home_menu, [], sys.argv[1:])


