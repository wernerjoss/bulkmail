#!/usr/bin/env python3
# derived from: https://www.pythonguis.com/tutorials/qprocess-external-programs/

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QFileDialog)

from PyQt5.QtCore import QProcess
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import bmgui_layout

class MainWindow(QMainWindow, bmgui_layout.Ui_MainWindow):
        
    def __init__(self):
        super().__init__()
        
        self.p = None
        self.MsgFile = 'message.txt'
        self.RecFile = 'reclist.lst'
        self.Attachment = ''
        self.setupUi(self)

        self.pushButton.pressed.connect(self.openRecFileDialog)
        self.pushButton_2.pressed.connect(self.openMsgFileDialog)
        self.pushButton_3.pressed.connect(self.start_process)
        self.pushButton_4.pressed.connect(self.openAttachmentDialog)
        
    def message(self, s):
        self.plainTextEdit.appendPlainText(s)

    def start_process(self):
        if self.p is None:  # No process running.
            #   self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            ArgList = ['bulkmail.py']
            if (self.checkBox.isChecked() == True):
                ArgList.append('-s')
            if (self.checkBox_2.isChecked() == True):
                ArgList.append('-l')
            if (self.checkBox_3.isChecked() == True):
                ArgList.append('-n')
            ArgList.append('-r')
            ArgList.append(self.RecFile)
            ArgList.append('-m')
            ArgList.append(self.MsgFile)
            if (len(self.Attachment) < 1):
                ArgList.append('-a')
                ArgList.append(self.Attachment)
            #   print(ArgList)
            self.p.start("python3", ArgList)  # JEDES arg extra !!
            
    def openAttachmentDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;All Files (*.*)", options=options)
        if fileName:
            #   print(fileName)
            self.Attachment = fileName
            self.message('Attachment: ' + self.Attachment)
    
    def openRecFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.lst)", options=options)
        if fileName:
            #   print(fileName)
            self.RecFile = fileName
            self.message('Recipient File: ' + self.RecFile)
    
    def openMsgFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            #   print(fileName)
            self.MsgFile = fileName
            self.message('Message File: ' + self.MsgFile)
    
    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        #   self.message(f"State changed: {state_name}")

    def process_finished(self):
        #   self.message("Process finished.")
        self.p = None

app = QApplication(sys.argv)

w = MainWindow()
#   w.resize(1440,1024)
title = "bmgui.py - Frontend for bulkmail.py (C) Werner Joss 2022"
w.setWindowTitle(title)

w.show()

app.setStyle("Fusion")
app.exec_()