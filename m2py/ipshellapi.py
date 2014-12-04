#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Caio Rodrigues
# @Date:   2014-11-16 12:35:32
# @Last Modified by:   wolfprogrammer
# @Last Modified time: 2014-11-16 12:55:57
#
# Ipython Shell Customization API
#
#
#---------------------------------------------------------


#from tabulate import tabulate
#from pprint import pprint

from IPython.terminal.embed import InteractiveShellEmbed
import os
import sys


class Ipshell:
    """
    IPython facade to create custom ipython
    shell easily and fast

    """

    def __init__(self, banner="", exitmsg="", listener=False, startdir=""):
        self.ipsh = InteractiveShellEmbed( banner1=banner, exit_msg=exitmsg, display_banner=True, user_ns={})
        self.IP = self.ipsh.get_ipython()
        self.listener = listener

        if startdir:
            os.chdir(startdir)

    def addpath(self, pathlist):
        map( sys.path.append, pathlist)

    def magic(self, name):
        """
        Decorator to register Ipython Magic
        """
        def wrap(f):
            self.ipsh.define_magic(name, f)
        return wrap

    def set_magic(self, name, function):
        """
        Register Ipython Magic
        """
        self.ipsh.define_magic(name, function)


    def get_magic(self, magic):
        return self.IP.magic(magic)

    def exec_magic(self, magicfunction):
        """
        Get Ipython Magic Function
        """
        return self.IP.magic(magicfunction)

    def exec_magics(self, magiclist):
        map(self.IP.magic, magiclist)


    def get_ipython(self):
        return self.IP


    def load_modules(self, modules, hidden=False):

        for module  in modules:
            object = __import__(module)
            self.ipsh.user_ns[module] = object

            if hidden:
                 self.ipsh.user_ns_hidden.add(module)



    def load_functions_from_module(self, module, objlist, hidden=False):

        module = __import__(module)

        #print "module = ", module
        #print self.ipsh.user_ns_hidden


        for objname in objlist:

            #print "objname ", objname

            obj = getattr(module, objname)
            #self.ipsh.user_ns_hidden[objname] = obj
            self.ipsh.user_ns[objname] = obj

            if hidden:
                self.ipsh.user_ns_hidden.add(objname)




    def load_objects(self, dic_objects):
        self.ipsh.user_ns.update(dic_objects)



    @property
    def user_ns(self):
        """
        Return User namespace
        """
        return self.IP.user_ns

    def autoreload(self, enable=True):
        """
        Set IPython shell to autoreload

        whenever you edit your file, your objects will
        be updated in ipython without the need to close
        and reopen ipython.
        """
        if enable:
            self.exec_magic("load_ext autoreload")
            self.exec_magic("autoreload 2")
        else:
            self.exec_magic("autoreload 0")

    def autocall(self, enable=True):
        """
        """
        if enable:
            self.exec_magic("autocall")
        else:
            self.exec_magic("autocall 0")

    def run(self):
        """
        Start Ipython Shell
        """
        #self.ipsh.define_magic("get_ipsh", get_ipsh)

        self.ipsh()

