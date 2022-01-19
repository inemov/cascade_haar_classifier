# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 18:01:28 2020

@author: Ivan Nemov
"""

import cv2
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class OpencvHaarSamplesWindow(QtWidgets.QMainWindow):

    def __init__(self, _quit_signal_message, parent=None):
        
        self._quit_signal_message = _quit_signal_message
        
        super(OpencvHaarSamplesWindow, self).__init__(parent)
        self.form_widget = FormWidget(self, self._quit_signal_message)
        _widget = QtWidgets.QWidget()
        _layout = QtWidgets.QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)
        self.resize(1000, 515)
        self.setWindowTitle("Create image samples from video")
        self.setWindowIcon(QtGui.QIcon(QtCore.QDir.currentPath()+'/OpenCV_logo.png'))
        self.quit = QtWidgets.QAction("Quit", self)
        self.quit.triggered.connect(self.closeEvent)
        
    def closeEvent(self, event):
        self.form_widget.exit_action_custom()
        event.ignore()
        
class FormWidget(QtWidgets.QWidget):
    
    def __init__(self, parent, _quit_signal_message):
        super(FormWidget, self).__init__(parent)
        self.__controls()
        self.__layout()
        self._quit_signal_message = _quit_signal_message

    def __controls(self):
        self.menu_bar=QtWidgets.QMenuBar()
        self.menu_bar.setFixedHeight(20)
        file_menu=self.menu_bar.addMenu("File")
        exit_action=QtWidgets.QAction('Exit',self)
        exit_action.triggered.connect(self.exit_action_custom)
        file_menu.addAction(exit_action)
        
        self.FrameBox = QtWidgets.QGroupBox(self)
        self.FrameBox.setObjectName("FrameBox")
        self.FrameBox.setTitle("Frame: ")
        self.FrameBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        self.FrameView=QtWidgets.QLabel(self.FrameBox)
        self.FrameView.setObjectName("FrameView")
        self.x_dim = 975
        self.y_dim = 470
        self.FrameViewPixmap = QtGui.QPixmap(QtCore.QDir.currentPath()+'/default_preview.png')
        self.FrameView.setPixmap(self.FrameViewPixmap.scaled(self.x_dim, self.y_dim))
        
        self.ControlsBox = QtWidgets.QGroupBox(self)
        self.ControlsBox.setObjectName("ControlsBox")
        self.ControlsBox.setTitle("")
        self.ControlsBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        self.Label_Source_File = QtWidgets.QLabel(self.ControlsBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Label_Source_File.setFont(font)
        self.Label_Source_File.setObjectName("Label_Source_File")
        self.Label_Source_File.setText("Select source file:         ")
        
        self.Source_File = QtWidgets.QLineEdit(self.ControlsBox)
        self.Source_File.setFixedHeight(25)
        
        self.Source_File_CommandButton = QtWidgets.QPushButton(self.ControlsBox)
        self.Source_File_CommandButton.setObjectName("Source_File_CommandButton")
        self.Source_File_CommandButton.setFixedWidth(80)
        self.Source_File_CommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Source_File_CommandButton.setText("Open")
        self.Source_File_CommandButton.clicked.connect(self.Source_File_manual_change)

        self.Label_Positive_Folder = QtWidgets.QLabel(self.ControlsBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Label_Positive_Folder.setFont(font)
        self.Label_Positive_Folder.setObjectName("Label_Positive_Folder")
        self.Label_Positive_Folder.setText("Select positive folder:  ")
        
        self.Positive_Folder = QtWidgets.QLineEdit(self.ControlsBox)
        self.Positive_Folder.setFixedHeight(25)
        directory = str(QtCore.QDir.currentPath() + "/positive/rawdata")
        self.Positive_Folder.setText(directory)
        
        self.Positive_Folder_CommandButton = QtWidgets.QPushButton(self.ControlsBox)
        self.Positive_Folder_CommandButton.setObjectName("Positive_Folder_CommandButton")
        self.Positive_Folder_CommandButton.setFixedWidth(80)
        self.Positive_Folder_CommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Positive_Folder_CommandButton.setText("Open")
        self.Positive_Folder_CommandButton.clicked.connect(self.Positive_Folder_manual_change)
        
        self.Label_Negative_Folder = QtWidgets.QLabel(self.ControlsBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Label_Negative_Folder.setFont(font)
        self.Label_Negative_Folder.setObjectName("Label_Negative_Folder")
        self.Label_Negative_Folder.setText("Select negative folder: ")
        
        self.Negative_Folder = QtWidgets.QLineEdit(self.ControlsBox)
        self.Negative_Folder.setFixedHeight(25)
        directory = str(QtCore.QDir.currentPath() + "/negative/rawdata")
        self.Negative_Folder.setText(directory)
        
        self.Negative_Folder_CommandButton = QtWidgets.QPushButton(self.ControlsBox)
        self.Negative_Folder_CommandButton.setObjectName("Negative_Folder_CommandButton")
        self.Negative_Folder_CommandButton.setFixedWidth(80)
        self.Negative_Folder_CommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Negative_Folder_CommandButton.setText("Open")
        self.Negative_Folder_CommandButton.clicked.connect(self.Negative_Folder_manual_change)

        self.PreviousButton = QtWidgets.QPushButton(self.ControlsBox)
        self.PreviousButton.setObjectName("PreviousButton")
        self.PreviousButton.setFixedWidth(100)
        self.PreviousButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PreviousButton.setText("Previous")
        self.PreviousButton.clicked.connect(self.previous_frame)
        
        self.NextButton = QtWidgets.QPushButton(self.ControlsBox)
        self.NextButton.setObjectName("NextButton")
        self.NextButton.setFixedWidth(100)
        self.NextButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NextButton.setText("Next")
        self.NextButton.clicked.connect(self.next_frame)
        
        self.SaveButton = QtWidgets.QPushButton(self.ControlsBox)
        self.SaveButton.setObjectName("SaveButton")
        self.SaveButton.setFixedWidth(100)
        self.SaveButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SaveButton.setText("Save")
        self.SaveButton.clicked.connect(self.save_image)
        
        self.AddROIButton = QtWidgets.QPushButton(self.ControlsBox)
        self.AddROIButton.setObjectName("AddROIButton")
        self.AddROIButton.setFixedWidth(150)
        self.AddROIButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddROIButton.setText("Add ROI")
        self.AddROIButton.clicked.connect(self.AddROI)
        
        self.RemoveROIButton = QtWidgets.QPushButton(self.ControlsBox)
        self.RemoveROIButton.setObjectName("RemoveROIButton")
        self.RemoveROIButton.setFixedWidth(150)
        self.RemoveROIButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RemoveROIButton.setText("Remove ROI")
        self.RemoveROIButton.clicked.connect(self.RemoveROI)
        
        self.Label_Resolution = QtWidgets.QLabel(self.ControlsBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.Label_Resolution.setFont(font)
        self.Label_Resolution.setObjectName("Label_Resolution")
        self.Label_Resolution.setText("Resolution: ")
        
        self.ResolutionDropDown=QtWidgets.QComboBox(self.ControlsBox)
        self.ResolutionDropDown.addItems(["16:9 - 1280x720", "16:9 - 1664x928", "16:9 - 1920x1088", "4:3 - 640x480", "4:3 - 1664x1232"])
        self.ResolutionDropDown.setMinimumWidth(80)
        
    def __layout(self):
        self.vmainbox=QtWidgets.QVBoxLayout()       
        self.hmenubox = QtWidgets.QHBoxLayout()
        self.hmenubox.addWidget(self.menu_bar)
        self.vgroupbox = QtWidgets.QVBoxLayout()
        self.vgroupbox.addWidget(self.FrameBox)
        self.vgroupbox.addWidget(self.ControlsBox)
        self.vmainbox.addLayout(self.hmenubox)
        self.vmainbox.addLayout(self.vgroupbox)
        self.setLayout(self.vmainbox)
        
        self.vFrameBox=QtWidgets.QVBoxLayout()
        self.vFrameBox.addWidget(self.FrameView)
        self.FrameBox.setLayout(self.vFrameBox)
        self.vFrameBox.setAlignment(self.FrameView, QtCore.Qt.AlignCenter)
        
        self.v1ControlBox=QtWidgets.QVBoxLayout()
        self.h1ControlBox=QtWidgets.QHBoxLayout()
        self.h1ControlBox.addWidget(self.Label_Source_File)
        self.h1ControlBox.addWidget(self.Source_File)
        self.h1ControlBox.addWidget(self.Source_File_CommandButton)
        self.h2ControlBox=QtWidgets.QHBoxLayout()
        self.h2ControlBox.addWidget(self.Label_Positive_Folder)
        self.h2ControlBox.addWidget(self.Positive_Folder)
        self.h2ControlBox.addWidget(self.Positive_Folder_CommandButton)
        self.h3ControlBox=QtWidgets.QHBoxLayout()
        self.h3ControlBox.addWidget(self.Label_Negative_Folder)
        self.h3ControlBox.addWidget(self.Negative_Folder)
        self.h3ControlBox.addWidget(self.Negative_Folder_CommandButton)
        self.v1ControlBox.addLayout(self.h1ControlBox)
        self.v1ControlBox.addLayout(self.h2ControlBox)
        self.v1ControlBox.addLayout(self.h3ControlBox)
        
        self.v2ControlBox=QtWidgets.QVBoxLayout()
        self.v2ControlBox.addWidget(self.PreviousButton)
        self.v2ControlBox.addWidget(self.NextButton)
        self.v2ControlBox.addWidget(self.SaveButton)
        
        self.v3ControlBox=QtWidgets.QVBoxLayout()
        self.h4ControlBox=QtWidgets.QHBoxLayout()
        self.h4ControlBox.addWidget(self.Label_Resolution)
        self.h4ControlBox.addWidget(self.ResolutionDropDown)
        self.h5ControlBox=QtWidgets.QHBoxLayout()
        self.h5ControlBox.addWidget(self.AddROIButton)
        self.h6ControlBox=QtWidgets.QHBoxLayout()
        self.h6ControlBox.addWidget(self.RemoveROIButton)
        self.v3ControlBox.addLayout(self.h4ControlBox)
        self.v3ControlBox.addLayout(self.h5ControlBox)
        self.v3ControlBox.addLayout(self.h6ControlBox)
        self.h4ControlBox.setAlignment(QtCore.Qt.AlignCenter)
        self.h5ControlBox.setAlignment(QtCore.Qt.AlignCenter)
        self.h6ControlBox.setAlignment(QtCore.Qt.AlignCenter)
        
        self.hControlsBox=QtWidgets.QHBoxLayout()
        self.hControlsBox.addLayout(self.v1ControlBox)
        self.hControlsBox.addLayout(self.v2ControlBox)
        self.hControlsBox.addLayout(self.v3ControlBox)
        self.ControlsBox.setLayout(self.hControlsBox)
        
        self.video = None
        self.count = 0
        self.ROI_array = []
        
    def previous_frame(self):
        if self.count<=1:
            return None
        
        try:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.count-2)
            successImage, image = self.video.read()
            imwidth, imheight = self.get_target_resolution()
            self.image = cv2.resize(image, (imwidth, imheight))
        except:
            return None
        
        if successImage:
            GUI_image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
            self.FrameViewPixmap = QtGui.QPixmap(GUI_image)
            self.draw_image()
            self.update_frame_title()
            self.count = self.count-1
            self.ROI_array = []
    
    def next_frame(self):
        if self.count>=self.total_frames:
            return None
        
        try:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.count)
            successImage, image = self.video.read()
            imwidth, imheight = self.get_target_resolution()
            self.image = cv2.resize(image, (imwidth, imheight))
        except:
            return None
        
        if successImage:
            GUI_image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
            self.FrameViewPixmap = QtGui.QPixmap(GUI_image)
            self.draw_image()
            self.update_frame_title()
            self.count = self.count+1
            self.ROI_array = []
    
    def save_image(self):
        try:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.count-1)
            successImage, image = self.video.read()
            imwidth, imheight = self.get_target_resolution()
            self.image = cv2.resize(image, (imwidth, imheight))
        except:
            return None
        source_file_path = self.Source_File.text()
        source_file_path_delim = source_file_path.split("/")
        source_file_name = source_file_path_delim[-1]
        source_file_name_ext = str("/" + str(source_file_name[:-4]) + "_" + str(self.count) + ".bmp")
        if self.ROI_array == []:
            image_file = str(self.Negative_Folder.text() + source_file_name_ext)
        else:
            image_file = str(self.Positive_Folder.text() + source_file_name_ext)
            with open(self.Positive_Folder.text()+"/info.txt", "a") as info_file:
                newstring = str("\\rawdata\\" + str(source_file_name[:-4]) + "_" + str(self.count) + ".bmp" + " " + str(len(self.ROI_array)))
                for targetObjectBox in self.ROI_array:
                    newstring = str(newstring + " " + str(targetObjectBox[0]) + " " + str(targetObjectBox[1]) + " " + str(targetObjectBox[2]) + " " + str(targetObjectBox[3]))
                info_file.write(str(newstring + "\n"))
        cv2.imwrite(image_file, self.image)
        
    def Source_File_manual_change(self):
        directory = str(QtCore.QDir.currentPath())
        file_filter = 'Video file (*.mp4)'
        file_name = str(QtWidgets.QFileDialog.getOpenFileName(self, "Select video file", directory, file_filter))
        file_name = file_name.split("'")[1]
        
        if not(os.path.isfile(file_name)):
            self.Source_File.setText("")
            return None
        try:
            self.video.release()
        except:
            self.video = None
        
        try:
            self.video = cv2.VideoCapture(file_name)
            successImage, image = self.video.read()
            imwidth, imheight = self.get_target_resolution()
            self.image = cv2.resize(image, (imwidth, imheight))
            self.fps = self.video.get(cv2.CAP_PROP_FPS)
            self.total_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        except:
            return None
        
        if successImage:
            GUI_image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
            self.FrameViewPixmap = QtGui.QPixmap(GUI_image)
            self.draw_image()
            self.update_frame_title()
            self.Source_File.setText(file_name)
            self.count = 1
            self.ROI_array = []
    
    def update_frame_title(self):
        self.FrameBox.setTitle(str("Frame: " + str(self.count) + " out of " + str(self.total_frames)))

    def Positive_Folder_manual_change(self):
        folder_name = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.Positive_Folder.setText(folder_name)
    
    def Negative_Folder_manual_change(self):
        folder_name = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.Negative_Folder.setText(folder_name)
    
    def AddROI(self):
        fromCenter = False
        showCrosshair = False
        try:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.count-1)
            successImage, image = self.video.read()
            imwidth, imheight = self.get_target_resolution()
            self.image = cv2.resize(image, (imwidth, imheight))
        except:
            return None
        temp_image = self.image
        targetObjectBox = cv2.selectROI('Select target', temp_image, fromCenter, showCrosshair)
        cv2.waitKey(30)
        cv2.destroyWindow('Select target')
        self.ROI_array.append(targetObjectBox)
        for targetObjectBox in self.ROI_array:
            cv2.rectangle(temp_image, (targetObjectBox[0], targetObjectBox[1]), (targetObjectBox[0]+targetObjectBox[2], targetObjectBox[1]+targetObjectBox[3]), (0,255,0), 2)
        GUI_image = QtGui.QImage(temp_image.data, temp_image.shape[1], temp_image.shape[0], QtGui.QImage.Format_RGB888)
        self.FrameViewPixmap = QtGui.QPixmap(GUI_image)
        self.draw_image()
    
    def RemoveROI(self):
        if self.ROI_array == []:
            return None
        elif len(self.ROI_array) == 1:
            self.ROI_array = []
            try:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, self.count-1)
                successImage, image = self.video.read()
                imwidth, imheight = self.get_target_resolution()
                self.image = cv2.resize(image, (imwidth, imheight))
            except:
                return None
            GUI_image = QtGui.QImage(self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888)
            self.FrameViewPixmap = QtGui.QPixmap(GUI_image)
            self.draw_image()
        else:
            self.ROI_array = self.ROI_array[:len(self.ROI_array)-1]
            try:
                self.video.set(cv2.CAP_PROP_POS_FRAMES, self.count-1)
                successImage, image = self.video.read()
                imwidth, imheight = self.get_target_resolution()
                self.image = cv2.resize(image, (imwidth, imheight))
            except:
                return None
            temp_image = self.image
            for targetObjectBox in self.ROI_array:
                cv2.rectangle(temp_image, (targetObjectBox[0], targetObjectBox[1]), (targetObjectBox[0]+targetObjectBox[2], targetObjectBox[1]+targetObjectBox[3]), (0,255,0), 2)
            GUI_image = QtGui.QImage(temp_image.data, temp_image.shape[1], temp_image.shape[0], QtGui.QImage.Format_RGB888)
            self.FrameViewPixmap = QtGui.QPixmap(GUI_image)
            self.draw_image()
        
        
    def get_target_resolution(self):
        image_resolution=str(self.ResolutionDropDown.currentText())
        if "1280x720" in image_resolution:
            imwidth = 1280
            imheight = 720
        elif "1664x928" in image_resolution:
            imwidth = 1664
            imheight = 928
        elif "1920x1088" in image_resolution:
            imwidth = 1920
            imheight = 1088
        elif "640x480" in image_resolution:
            imwidth = 640
            imheight = 480
        elif "1664x1232" in image_resolution:
            imwidth = 1664
            imheight = 1232
        return(imwidth,imheight)
                
    def resizeEvent(self, event):
        self.x_dim = self.FrameBox.frameGeometry().width()-25
        self.y_dim = self.FrameBox.frameGeometry().height()-45
        imwidth, imheight = self.get_target_resolution()
        if self.x_dim*imheight/imwidth < self.y_dim:
            self.y_dim = self.x_dim*imheight/imwidth
        elif self.y_dim*imwidth/imheight < self.x_dim:
            self.x_dim = self.y_dim*imwidth/imheight
        self.draw_image()
        
    def draw_image(self):
        try:
            self.FrameView.setPixmap(self.FrameViewPixmap.scaled(self.x_dim, self.y_dim))
        except:
            return None
        
    def exit_action_custom(self):
        try:
            self.video.release()
            self.video = None
            self._quit_signal_message.quit_signal_message_bit.emit(True)
        except:
            self.video = None
            self._quit_signal_message.quit_signal_message_bit.emit(True)

class quit_signal_message(QtCore.QObject):
    quit_signal_message_bit = QtCore.pyqtSignal(bool)
        
def call(_quit_signal_message):
    OpencvHaarSamples_window = OpencvHaarSamplesWindow(_quit_signal_message)
    OpencvHaarSamples_window.show()
    return OpencvHaarSamples_window