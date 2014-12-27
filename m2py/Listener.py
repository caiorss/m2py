#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

class Listener():

    def __init__(self, host='', port=8888):

        import socket
        import sys

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
        import inspect
        import socket
        s= self.sock

        try:
            s.bind((self.host, self.port))
        except socket.error as msg:
            print(('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]))
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
                print((err.args))
                print((err.__class__))

    def main(self):

        import threading

        server_thread = threading.Thread(target=self._main, args=())
        server_thread.daemon =True
        server_thread.start()

