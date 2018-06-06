# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadingView.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoadingView(object):
    def setupUi(self, LoadingView):
        LoadingView.setObjectName("LoadingView")
        LoadingView.resize(584, 388)
        self.gridLayout = QtWidgets.QGridLayout(LoadingView)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_Exit = QtWidgets.QPushButton(LoadingView)
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.gridLayout.addWidget(self.pushButton_Exit, 2, 0, 1, 1)
        self.plainTextEdit_LoadingState = QtWidgets.QPlainTextEdit(LoadingView)
        self.plainTextEdit_LoadingState.setObjectName("plainTextEdit_LoadingState")
        self.gridLayout.addWidget(self.plainTextEdit_LoadingState, 1, 0, 1, 7)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 6)
        self.label = QtWidgets.QLabel(LoadingView)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(LoadingView)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 0, 1, 1, 6)

        self.retranslateUi(LoadingView)
        QtCore.QMetaObject.connectSlotsByName(LoadingView)

    def retranslateUi(self, LoadingView):
        _translate = QtCore.QCoreApplication.translate
        LoadingView.setWindowTitle(_translate("LoadingView", "加载LIDC-IDRI"))
        self.pushButton_Exit.setText(_translate("LoadingView", "关闭"))
        self.label.setText(_translate("LoadingView", "加载进度:"))

