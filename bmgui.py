#!/usr/bin/env python3
# derived from: https://www.pythonguis.com/tutorials/qprocess-external-programs/

from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QFileDialog)

from PyQt6.QtCore import QProcess
import sys, os
from PyQt6 import QtCore, QtGui, QtWidgets
import bmgui_layout
import yaml
import webbrowser

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
        self.pushButton_5.pressed.connect(self.help)
        # read config from yaml file:
        cfgpath = os.path.abspath(os.path.dirname(__file__))
        try:
            cfgfile = cfgpath + '/bulkmail.yaml'	# config file must reside in same Dir as Program !
            with open(cfgfile, "r") as configfile:
                cfg = yaml.load(configfile, Loader=yaml.FullLoader)
                configfile.close()
        except:	# Defaults:
            cfg = {
                'FROM': 'George Bush <ghwbush@whitehouse.gov>',
                'smtp_server': 'smtp1.whitehouse.gov',
                'user': 'gbush',
                'pwd': 'obama',
                'editor': 'kate'
            }
        try:
            self.editor = cfg['editor']
        except:
            self.editor = 'kate'
        
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
            expath = os.path.abspath(os.path.dirname(__file__))
            exfile = expath + '/bulkmail.py'    # CLI Version must reside in same Dir as GUI Version !
            ArgList = [exfile]
            if (self.checkBox.isChecked() == True):
                ArgList.append('-s')
            if (self.checkBox_2.isChecked() == True):
                ArgList.append('-l')
            if (self.checkBox_3.isChecked() == True):
                ArgList.append('-n')
            if (self.checkBox_4.isChecked() == True):
                ArgList.append('-p')
            Delay = 0
            if (self.spinBox.value() > 0):
                Delay = self.spinBox.value()
                # self.message("Delay:" + str(Delay))
                ArgList.append('-d')
                ArgList.append(str(Delay))
            ArgList.append('-r')
            ArgList.append(self.RecFile)
            ArgList.append('-m')
            ArgList.append(self.MsgFile)
            if (len(self.Attachment) > 1):
                ArgList.append('-a')
                ArgList.append(self.Attachment)
            print(ArgList)
            self.p.start("python3", ArgList)  # JEDES arg extra !!
            
    def openAttachmentDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "*.*","All Files (*.*)")
        if fileName:
            #   print(fileName)
            self.Attachment = fileName
            self.message('Attachment: ' + self.Attachment)
    
    def openRecFileDialog(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("List Files (*.lst *.txt)")
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        if dialog.exec():
            #   print(fileName)
            selected_files = file_names = dialog.selectedFiles()  #fileName
            self.RecFile = selected_files[0]
            self.message('Recipient File: ' + self.RecFile)
            if self.p is None:
                self.p = QProcess()
                self.p.finished.connect(self.process_finished)  # Clean up once complete.
                self.p.start(self.editor, [self.RecFile])
    
    def openMsgFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "*.txt","Text Files (*.txt)")
        if fileName:
            #   print(fileName)
            self.MsgFile = fileName
            self.message('Message File: ' + self.MsgFile)
            if self.p is None:
                self.p = QProcess()
                self.p.finished.connect(self.process_finished)  # Clean up once complete.
                self.p.start(self.editor, [self.MsgFile])
    
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
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running',
        }
        state_name = states[state]
        #   self.message(f"State changed: {state_name}")

    def help(self):
        browser = webbrowser.get()
        Link = "https://github.com/wernerjoss/bulkmail/blob/main/README.md"
        browser.open_new(Link)

    def process_finished(self):
        #   self.message("Process finished.")
        self.p = None
    
app = QApplication(sys.argv)

w = MainWindow()
#   w.resize(1440,1024)
title = "bmgui.py v 0.1.5 - Frontend for bulkmail.py (C) Werner Joss 2025"
w.setWindowTitle(title)

w.show()

app.setStyle("Fusion")
app.exec()