# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 548)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.search_b = QtWidgets.QPushButton(self.centralwidget)
        self.search_b.setObjectName("search_b")
        self.horizontalLayout_2.addWidget(self.search_b)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ol_cb = QtWidgets.QCheckBox(self.centralwidget)
        self.ol_cb.setChecked(True)
        self.ol_cb.setObjectName("ol_cb")
        self.horizontalLayout.addWidget(self.ol_cb)
        self.intro_rb = QtWidgets.QRadioButton(self.centralwidget)
        self.intro_rb.setObjectName("intro_rb")
        self.horizontalLayout.addWidget(self.intro_rb)
        self.detail_rb = QtWidgets.QRadioButton(self.centralwidget)
        self.detail_rb.setChecked(True)
        self.detail_rb.setObjectName("detail_rb")
        self.horizontalLayout.addWidget(self.detail_rb)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.textBrowser.setFont(font)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wudao"))
        self.search_b.setText(_translate("MainWindow", "SEARCH"))
        self.ol_cb.setText(_translate("MainWindow", "Online"))
        self.intro_rb.setText(_translate("MainWindow", "introduction"))
        self.detail_rb.setText(_translate("MainWindow", "detailed"))

