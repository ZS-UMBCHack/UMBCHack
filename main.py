# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 21:17:02 2020

@author: Sophie
"""

import PyQt5.QtWidgets as wd
# import PyQt5.QtCore as cr
import sys

class Window(wd.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(300,300,600,400)
        self.setWindowTitle("Test")
        self.show()
        
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        
        exit_action = wd.QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        
        self.file_menu.addAction(exit_action)

if __name__ == "__main__":     
    app = wd.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

# label = wd.QLabel("Hello World!")
# label.show()