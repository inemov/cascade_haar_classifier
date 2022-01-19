# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 20:10:04 2020

@author: Ivan Nemov
"""

from PyQt5 import QtCore
import os

directory = str(QtCore.QDir.currentPath() + "/rawdata")
files = os.listdir(directory)
bg_file_name = str(QtCore.QDir.currentPath() + "/bg.txt")
with open(bg_file_name, "a") as bg_file:
    for file_name in files:
        bg_file.write("\\rawdata\\" + str(file_name) + "\n")

