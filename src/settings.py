
''' Grammar for a menu

menu : list(item)
item: tuple(title, action)
title: string
action: menu | shellcommand
shellcommand: string
'''



''' Constants '''

# Self-update info
appdir = '/usr/bin'
appfile_in = 'menu.py'
appfile_out = 'admin'
configfile_in = 'settings.py'
configfile_out = 'settings.py'
selfupdate_url = 'https://github.com/jc2brown/QuickMenu/tarball/master'
selfupdate_tarfile = 'master'
selfupdate_untarpath = 'jc2brown-QuickMenu-*'''




'''
Menu Items

The program will look for home_menu. This is the only required item. 
'''


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
#selfupdate_cmd = '''
#    svn co svn://jc2brown.ca/svn/QuickMenu/trunk/src;
#    mv -f src/menu.py /usr/bin/menu;
#    chmod +x /usr/bin/menu; 
#    rm -rf src;
#'''

selfupdate_cmd = '''
    wget -O menu.tar '''+selfupdate_url+''';
    tar -xvf menu.tar;
    mv '''+selfupdate_untarpath+'''/src/'''+appfile_in+''' '''+appdir+'''/'''+appfile_out+''';
    mv '''+selfupdate_untarpath+'''/src/'''+configfile_in+''' '''+appdir+'''/'''+configfile_out+''';
    chmod +x '''+appdir+'''/'''+appfile_out+''';
    rm -rf '''+selfupdate_untarpath+''';
'''
    

home_menu = [
             ('System', system_menu),
             ('Apache2', apache2_menu),
             ('Tomcat7', tomcat7_menu),
             ('Cloud', cloud_menu),
             ('Self-Update', selfupdate_cmd)
             ]

