#!/usr/bin/env python3
# derived from: https://www.pythonguis.com/tutorials/qprocess-external-programs/

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QFileDialog)

from PyQt5.QtCore import QProcess
import sys

class MainWindow(QMainWindow):
        
    def __init__(self):
        super().__init__()

        self.p = None
        self.MsgFile = 'message.txt'
        self.RecFile = 'reclist.lst'
    
        self.selRecFilebtn = QPushButton("Select Recipients File")
        self.selRecFilebtn.pressed.connect(self.openRecFileDialog)
        self.selMsgFilebtn = QPushButton("Select MessageFile")
        self.selMsgFilebtn.pressed.connect(self.openMsgFileDialog)
        self.btn = QPushButton("Execute")
        self.btn.pressed.connect(self.start_process)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        
        l = QVBoxLayout()
        l.addWidget(self.selRecFilebtn)
        l.addWidget(self.selMsgFilebtn)
        l.addWidget(self.btn)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)
        
        self.setCentralWidget(w)

    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        if self.p is None:  # No process running.
            #   self.message("Executing process")
            self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.stateChanged.connect(self.handle_state)
            self.p.finished.connect(self.process_finished)  # Clean up once complete.
            recipients = '-r ' + self.RecFile
            msg = '-m ' + self.MsgFile
            args = '-s ' + recipients + ' ' + msg
            self.p.start("python3", ['bulkmail.py', '-s', '-r', self.RecFile, '-m', self.MsgFile])  # JEDES arg extra !!

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
w.resize(1440,1024)
w.show()

app.exec_()