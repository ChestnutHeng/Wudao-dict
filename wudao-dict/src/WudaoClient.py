# -*- coding: utf-8 -*-

import socket
import time
import os
import logging


class WudaoClient:
    def __init__(self):
        self.client = None
        self.RED_PATTERN = '\033[31m%s\033[0m'
        logging.basicConfig(filename='./user/client.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    def connect(self):
        # waiting for server init
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
        beats, count = 0, 0
        while True:
            try:
                self.client.connect(("127.0.0.1", 23764))
                break
            except ConnectionRefusedError:
                if count <= 3:
                    if beats >= 10:
                        print(self.RED_PATTERN % 'Error: Connection out of time!\nMaybe server is not up?\nCalling up server...\n')
                        logging.error('Connection out of time, calling up server...')
                        os.system('python3 WudaoServer.py &') # try to call up server
                        beats = 0
                        count += 1
                    time.sleep(0.1)
                    beats += 1
                else:
                    print(self.RED_PATTERN % 'Failed to call up server! Exiting!\n')
                    logging.ERROR('Failed to call up server. Exiting!')
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
            logging.info('Server closed!')
