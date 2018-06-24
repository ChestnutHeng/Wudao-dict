#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import sys
import logging
import threading

from src.DictReader import DictReader
from src.tools import is_alphabet
from src.tools import ie
from src.tools import get_ip
from src.tools import report_new_word
from src.tools import report_old_word


class WudaoServer (threading.Thread):
    def __init__(self, threadID, threadName):
        # multithread
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName

        self.dict_reader = DictReader()
        self.ip = get_ip()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Define socket
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logging.basicConfig(filename='./user/server.log', level=logging.ERROR, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        # Singleton
        try:
            self.server.bind(("0.0.0.0", 23764))
        except OSError:
            logging.error('OSError: Port has been used.')
            exit(0)
        self.server.listen(0)
        logging.info('Server on...')

    def run(self):
        while True:
            # Get bytes
            conn, addr = self.server.accept()
            data = conn.recv(256)
            word = data.decode('utf-8').strip()
            logging.info('Get:' + str(len(data)) + ' bytes ' + word)
            # Shutdown
            if word == '---shutdown keyword---':
                self.server.close()
                logging.info('Server Close\nBye!~~~')
                sys.exit(0)
            # Get word
            try:
                word_info = None
                if word:
                    if is_alphabet(word[0]):
                        word_info = self.dict_reader.get_word_info(word)
                    else:
                        word_info = self.dict_reader.get_zh_word_info(word)
                if word_info is not None:
                    conn.sendall(word_info.encode('utf-8'))
                    logging.info('Send: ' + str(len(word_info)) + ' bytes ')
                else:
                    conn.sendall('None'.encode('utf-8'))
            except KeyError:
                logging.error('No words: ' + word)
            conn.close()
            # report
            try:
                if ie():
                    if word_info is None:
                        report_new_word(word, self.ip)
                        logging.error('report new word')
                    else:
                        report_old_word(word, self.ip)
                        logging.error('report old word')
                else:
                    logging.error('no ie, report failed')
            except:
                logging.error('exception occured, report failed')

def main():
    thread = WudaoServer(1, 'WudaoServer')
    thread.start()

if __name__ == '__main__':
    ws = WudaoServer()
    ws.run()

