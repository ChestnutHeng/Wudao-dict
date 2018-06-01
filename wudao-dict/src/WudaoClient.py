# -*- coding: utf-8 -*-

import socket
import time
import os


class WudaoClient:
    def __init__(self):
        self.client = None
        self.RED_PATTERN = '\033[31m%s\033[0m'

    def connect(self):
        # waiting for server init
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        beats, count = 0, 0
        while True:
            try:
                self.client.connect(("127.0.0.1", 23764))
                break
            except ConnectionRefusedError:
                if count <= 3:
                    if beats >= 20:
                        print(self.RED_PATTERN % 'Error: Connection out of time!\nMaybe server is not up?\nCalling up server...\n')
                        os.system('nohup python3 WudaoServer.py > ./usr/server.log 2>&1 &') # try to call up server
                        beats = 0
                        count += 1
                    time.sleep(0.2)
                    beats += 1
                else:
                    print(self.RED_PATTERN % 'Failed to call up server! Exiting!\n')
                    exit(1)

    def get_word_info(self, word):
        self.connect()
        word = word.lower()
        self.client.sendall(word.encode('utf-8'))
        server_context = b''
        while True:
            rec = self.client.recv(512)
            if not rec:
                break
            server_context += rec
        server_context = server_context.decode('utf-8')
        self.client.close()
        return server_context

    def close(self):
        self.connect()
        if self.client:
            self.client.sendall('---shutdown keyword---'.encode('utf-8'))
            print('Server closed!')
