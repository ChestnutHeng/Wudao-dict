# -*- coding: utf-8 -*-

import socket
import time


class WudaoClient:
    def __init__(self):
        self.client = None

    def connect(self):
        # waiting for server init
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        beats = 0
        while True:
            try:
                self.client.connect(("127.0.0.1", 23764))
                break
            except ConnectionRefusedError:
                if beats >= 20:
                    print('Error: Connection out of time')
                    break
                time.sleep(0.2)
                beats += 1

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
