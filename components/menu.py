from PyQt5.QtWidgets import (
  QFileDialog, QAction, QMenuBar, QMenu
)
from PyQt5.QtCore import QEvent
import os
import webbrowser
import shutil
import sys
import subprocess

from components.myfunc import getPath
from dialogs.about import AboutDialog
from dialogs.ocr import OcrListDialog

class MenuBar(QMenuBar):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.parent = parent
    
    # File menu
    file = QMenu("Files", self)
    saveAs = QAction("Save As", self)
    saveAs.triggered.connect(self.saveAs)
    
    restart = QAction("Restart", self)
    restart.triggered.connect(self.restart)
    
    exit = QAction("Exit", self)
    exit.triggered.connect(parent.close)
    
    
    file.addAction(saveAs)
    file.addAction(restart)
    file.addAction(exit)
    
    # OCR Menu
    ocr = QMenu('OCR', self)
    uploadOcr = QAction('Upload', self)
    uploadOcr.triggered.connect(self.uploadOcr)
    
    findOcr = QAction('Find OCR', self)
    findOcr.triggered.connect(self.openOcrWebpage)

    ocrList = QAction('OCR List', self)
    ocrList.triggered.connect(self.openOcrList)
    
    ocr.addActions([ocrList, uploadOcr, findOcr])

    about = QMenu('About', self)
    aboutAction = QAction('About', self)
    aboutAction.triggered.connect(self.openAbout)

    about.addActions([aboutAction])
    
    self.addMenu(file)
    self.addMenu(ocr)
    self.addMenu(about)

  def saveAs(self):
    filePath, _ = QFileDialog.getSaveFileName(self, "Save file as", self.parent.setting.value('lastPath', '~'), 'Text Files (*.txt)')
    if filePath:
      root, ext = os.path.splitext(filePath)
      if ext == '':
        filepath += '.txt'
        
      text = self.parent.textOutput.toPlainText()
      with open(filePath, 'w', encoding='utf-8') as f:
        f.write(text)
        
  def restart(self):
    subprocess.Popen([sys.executable] + sys.argv)
    sys.exit()
        
  def uploadOcr(self):
    filePath, _ = QFileDialog.getOpenFileName(self, 'Upload ocr', self.parent.setting.value('lastPath', '~'), 'Trained data (*.traineddata)')
    if (filePath):
      target = getPath(os.path.join('Tesseract-OCR', 'tessdata'))
      shutil.copy(filePath, target)

  def openOcrWebpage(self):
    webbrowser.open('https://github.com/tesseract-ocr/tessdata')

  def openAbout(self):
    dialog = AboutDialog()
    dialog.exec_()
  
  def openOcrList(self):
    dialog = OcrListDialog()
    dialog.exec_()