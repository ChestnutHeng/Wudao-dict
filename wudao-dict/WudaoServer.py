#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys

from src.JsonReader import JsonReader
from src.tools import is_alphabet
from src.tools import ie
from src.tools import get_ip
from src.tools import report_new_word
from src.tools import report_old_word


class WudaoServer:
    def __init__(self):
        self.json_reader = JsonReader()
        self.ip = get_ip()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Singleton
        try:
            self.server.bind(("0.0.0.0", 23764))
        except OSError:
            print('OSError: Port has been used.')
            exit(0)
        self.server.listen(0)
        print('Server on...')

    def run(self):
        while True:
            # Get bytes
            conn, addr = self.server.accept()
            data = conn.recv(256)
            word = data.decode('utf-8').strip()
            print('Get:' + str(len(data)) + ' bytes ' + word)
            # Shutdown
            if word == '---shutdown keyword---':
                self.server.close()
                print('Bye!~~~')
                sys.exit(0)
            # Get word
            try:
                word_info = None
                if word:
                    if is_alphabet(word[0]):
                        word_info = self.json_reader.get_word_info(word)
                    else:
                        word_info = self.json_reader.get_zh_word_info(word)
                if word_info is not None:
                    conn.sendall(word_info.encode('utf-8'))
                    print('Send: ' + str(len(word_info)) + ' bytes ')
                else:
                    conn.sendall('None'.encode('utf-8'))
            except KeyError:
                print('No words: ' + word)
            conn.close()
            # report
            # 停止扩充词典
            # try:
            #     if ie():
            #         if word_info is None:
            #             report_new_word(word, self.ip)
            #             print('report new word')
            #         else:
            #             report_old_word(word, self.ip)
            #             print('report old word')
            #     else:
            #         print('no ie, report failed')
            # except:
            #     print('exception occured, report failed')


if __name__ == '__main__':
    ws = WudaoServer()
    ws.run()

