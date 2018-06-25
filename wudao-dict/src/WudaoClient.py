# -*- coding: utf-8 -*-

import socket
import time
import logging
import threading
import src.WudaoServer

class WudaoClient:
    def __init__(self):
        self.client = None
        self.RED_PATTERN = '\033[31m%s\033[0m'
        self.ws = src.WudaoServer
        logging.basicConfig(filename='./user/client.log', level=logging.ERROR, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    def connect(self):
        # waiting for server init
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
        beats, count = 0, 0
        while True:
            try:
                self.client.connect(("127.0.0.1", 23764))
                break
            except ConnectionRefusedError:
                if beats >= 10:
                    print(self.RED_PATTERN % 'Error: Connection out of time!')
                    logging.error('Connection out of time!')
                    exit(1)
                time.sleep(0.2)
                beats += 1

    def get_word_info(self, word):
        #self.ws.main() # Call up server
        #self.connect()
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
        try:
            self.connect()
        except ConnectionError:
            exit(0)
        if self.client:
            self.client.sendall('---shutdown keyword---'.encode('utf-8'))
            logging.info('Server closed!')
