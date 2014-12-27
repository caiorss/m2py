#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A wraper to IPython to make calculation easier
like Matlab(R)

"""



__author__ = "Caio Rodrigues Soares Silva"

# Matplotlib intercative
# non-blocking

from IPython.terminal.embed import InteractiveShellEmbed

from .engine import *


class Listener():

    def __init__(self, host='', port=8888):

        import socket

        self.namespace = None

        self.host = host   # Symbolic name, meaning all available interfaces
        self.port = port   # Arbitrary non-privileged port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #s.settimeout(1)
        #print 'Socket created'

        #Bind socket to local host and port
        self.sock = s


    def _main(self):

        #logger.warn("Starting socket server")
        #import inspect
        import socket
        s= self.sock

        try:
            s.bind((self.host, self.port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            pass
            #sys.exit()

        #Start listening on socket
        s.listen(10)

        while True:
            conn, addr = self.sock.accept()
            code = conn.recv(8049)
            conn.close()
            
    
            #_globals = inspect.currentframe().f_back.f_globals

            code = '\n' + code
            print(code)

            try:
                bytecode = compile(code, '<string>', 'exec')
                exec (bytecode, globals())
            except Exception as err:
                print(err)
                print(err.args)
                print(err.__class__)

    def main(self):

        import threading

        server_thread = threading.Thread(target=self._main, args=())
        server_thread.daemon =True
        server_thread.start()

def __guide(self, arg):
    """
    Show a Ipython cheatsheet
    with examples

    """

    print("""
Quick Ipython Guide


HISTORY

* history with lines
     hist -n

* history with lines and output
     hist -n -o

* History converted in valid python
  source code
     hist -n -t

* Save history to file
     hist <line-range> -f <file>
     hist 1-10 -f h1.py

* Rerun previous commmand/input
     rerun

* Rerun line(s)
     rerun <line-range>

* Edit history lines in vim and execute
    edit 2-10

* Run py script
    run script.py

*

SESSIONS

create a macro called mac out of lines 1, 2, 3, 4,
and 7 of the history
    macro mac 1-4 7

runs the macro called mac
    mac

print mac       prints the commands in "c">mac
store mac       stores the macro in the profile, it will be available next time you start IPython
store x             store x in the profile. It will be loaded next time you start IPython.
store x > /tmp/a.txt    store x in the file, a.txt
store -r        restore into the workspace the variables that have been stored. Overwrites exisiting variables in workspace.
store -d x      delete just x from
storage
store -z        remove ALL variables from storage


LOGGING

logstate        show state of the logger (on or off)
logstart        start logging (default log file is ipython_log.py, in the present working directory
logstart filename   store history up to this point, and continue logging history, in filename
logstart -r filename    same as above, but use the raw input: don’t put the _ip.magic() wrapper around magic commands
logon           start logging after stopping
logoff          stop logging after starting
runlog log1 log2    run the log file log1, then run the log file log2 (this executes the logged histories)


DOCUMENTATION AND CODE INSTROSPECTION

Display functin help
    ? <function>

Print Docstring of object
    pdoc <object>

Pfile -  Print through pager where the object is defined
    pfile <object>

pinfo - Print information about object
    pinfo <object>


pinfo2 - Print detailed information about object
    pinfo2 <object>

psource - Print source code in through pager
    psource <object>


OBJECTIVES
    who    - Print a list of all interactive variables
    whos_l - Print a list of interactive variables
    whos   - Print extra information about variables


CUSTOM LISTING

    functions - List all functions
    values    - List all numeric variables ( Calculated values)
    arrays    - List all array variables
    strings   - List all string variables

""")



# Start directory
HOMEDIR = os.path.expanduser('~')
# os.chdir(HOMEDIR)

# Save log session log file automatically
#--------------------------
#__logdir = "/tmp/pylogs"
#os.system('mkdir -p ' + __logdir )
#__logfile = os.path.join(__logdir, 'log' + datetime.now().strftime('%y-%m-%d-%H-%M') + '.py')

# Banner and exit message
#------------------------------
banner = \
    """--- IPYTHON MATH LAB ENVIRONMENT ----\n
    To see the ipython cheat-sheet type:
    $  guide()
    
    Standard objects and modules
    
        -> xsteam:    Water Steam Table using NIST equations
        -> factor:    Units convertion factor, example MPA/psi
        -> units :    Unist factor and conversion functions
        -> constants: Physical Constants
        
    Angle Trigonometric Functions in degrees
    
    cosd, sind, atand, atand2, deg2rad, rad2deg, 

    """
exit_msg = "*** logfile: %s ***" 
# First import the embed function



ipshell = InteractiveShellEmbed(banner1=banner, exit_msg=exit_msg)
IP = ipshell.get_ipython()


def __setprec2(n):
    formt= '%' +'.%sf' % n
    #get_ipython().magic('precision '+formt)
    IP.magic('precision '+formt)    

def __setprec(self, n, type="fix"):
    """
    Set IPython Shell number of decimal places
    
    :param n: Maximum number of decimal places to be displayed
    :type  n: int
    :return:
    """
    if type == 'fix':
        base = '.%sf'
    
    formt= '%' + base % n
    #get_ipython().magic('precision '+formt)
    IP.magic('precision '+formt)

def include(filename):
    if os.path.exists(filename):
        exec(compile(open(filename).read(), filename, 'exec'))

def list_values(self, arg):
    """
    List all numeric types
    """
    IP.magic('whos int float float64 ndarray')

def list_arrays(self, arg):
    """
    Show all ndarrays
    """
    IP.magic('whos ndarray')

def list_lists(self, arg):
    """
    Show all lists objects
    """
    IP.magic('whos list')

def list_strings(self, arg):
    IP.magic('whos str')

def list_functions(self, arg):
    IP.magic('whos function')

ipshell.define_magic('values', list_values)
ipshell.define_magic('arrays', list_arrays)
ipshell.define_magic('functions', list_functions)
ipshell.define_magic('strings', list_strings)
ipshell.define_magic('lists', list_lists)
ipshell.define_magic('guide', __guide)
ipshell.define_magic('setprec', __setprec)


import argparse



#import IPython 
#from Listener import Listener 

# Daemon server to listen for python code
# from localhost

#    IPython.embed()


def main():
    
    pyserver = Listener()
    #pyserver.namespace = globals()
    pyserver.main()


    desc = " Python Mathematic Lab Environment "
    parser = argparse.ArgumentParser(prog='mathpy', description=desc)

 
    __setprec2(4)
    ipshell()

    #if args.runfile:
    #    print "Run script %s" % args.runfile
    #    #include(args.runfile)
    #    execfile(args.runfile)
    #    ipshell()

        #sys.exit(0)

if __name__ == "__main__":
    main()

    # IP.magic('logstart ' + __logfile)
    # ipshell()

