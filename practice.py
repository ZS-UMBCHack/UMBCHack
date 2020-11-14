# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 21:51:14 2020

@author: Sophie
"""

import PyQt5.QtWidgets as qt
import sys

class Window(qt.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(300,300,600,400)
        self.setWindowTitle("Test")
        self.show()
        
app = qt.QApplication(sys.argv)
window = Window()
label = qt.QLabel("Hello World!")
label.show()
sys.exit(app.exec_())