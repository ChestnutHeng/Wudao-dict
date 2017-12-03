from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import json

from mainwindow_ui import Ui_MainWindow
from src.GuiDraw import GuiDraw
from src.WudaoClient import WudaoClient
from src.tools import is_alphabet
from src.UserHistory import UserHistory


class MainWindow(QMainWindow):
    ui = None
    mainWindow = None
    client = WudaoClient()
    painter = GuiDraw()
    draw_conf = True
    is_zh = False
    word = ''

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.history_manager = UserHistory()
        self.setup_ui()

    def setup_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # auto complete
        self.auto_com_init()
        self.ui.ol_cb.setChecked(False)
        darkula = QPalette()
        # theme
        darkula.setColor(QPalette.Background, QColor('#300A24'))
        darkula.setColor(QPalette.Base, QColor('#300A24'))
        self.ui.textBrowser.setPalette(darkula)
        # status bar
        self.ui.statusbar.showMessage('@2016 Chestnut Studio')
        # signal slot
        self.ui.lineEdit.returnPressed.connect(self.search_bt_clicked)
        self.ui.search_b.clicked.connect(self.search_bt_clicked)
        self.ui.detail_rb.clicked.connect(self.detail_rb_clicked)
        self.ui.intro_rb.clicked.connect(self.intro_rb_clicked)

    def detail_rb_clicked(self):
        self.draw_conf = True
        self.search_bt_clicked()

    def intro_rb_clicked(self):
        self.draw_conf = False
        self.search_bt_clicked()

    # auto complete
    def auto_com_init(self):
        sl = ['a', 'air', 'airplane']
        com = QCompleter(sl)
        com.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.lineEdit.setCompleter(com)

    def search_bt_clicked(self):
        self.word = self.ui.lineEdit.text().strip()
        if self.word:
            # if chinese
            if is_alphabet(self.word[0]):
                self.is_zh = False
            else:
                self.is_zh = True
            # query on server
            server_context = self.client.get_word_info(self.word).strip()
            if server_context != 'None':
                wi = json.loads(server_context)
                self.painter.html = ''
                if self.is_zh:
                    self.painter.draw_zh_text(wi, self.draw_conf)
                else:
                    self.history_manager.add_item(self.word)
                    self.painter.draw_text(wi, self.draw_conf)
                self.ui.textBrowser.setHtml(self.painter.html)
            else:
                # Online search
                html = ''
                if self.ui.ol_cb.isChecked():
                    self.painter.html = ''
                    try:
                        self.ui.textBrowser.setHtml(self.painter.P_W_PATTERN % 'Searching OL...')
                        from src.WudaoOnline import get_text, get_zh_text
                        from urllib.error import URLError
                        if self.is_zh:
                            word_info = get_zh_text(self.word)
                        else:
                            word_info = get_text(self.word)
                        if not word_info['paraphrase']:
                            html += self.painter.P_W_PATTERN % ('No such word: %s found online' % self.word)
                        if not self.is_zh:
                            self.history_manager.add_word_info(word_info)
                            self.painter.draw_text(word_info, self.draw_conf)
                        else:
                            self.painter.draw_zh_text(word_info, self.draw_conf)
                        self.ui.textBrowser.setHtml(self.painter.html)
                        return
                    except ImportError:
                        html += self.painter.P_W_PATTERN % 'You need install bs4 first.'
                        html += self.painter.P_W_PATTERN % 'Use \'pip3 install bs4\' or get bs4 online.'
                    except URLError:
                        html += self.painter.P_W_PATTERN % 'No Internet : Please check your connection first'
                else:
                    # search in online cache first
                    word_info = self.history_manager.get_word_info(self.word)
                    if word_info:
                        self.history_manager.add_item(self.word)
                        self.painter.draw_text(word_info, self.draw_conf)
                        self.ui.textBrowser.setHtml(self.painter.html)
                        return
                    else:
                        html += self.painter.P_W_PATTERN % ('Error: no such word :' + self.word)
                        html += self.painter.P_W_PATTERN % 'You can check Online Box to search it online.'
                self.ui.textBrowser.setHtml(html)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
