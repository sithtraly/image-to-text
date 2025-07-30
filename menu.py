from PyQt5.QtWidgets import (
  QFileDialog, QAction, QMenuBar, QMenu
)
import os
import webbrowser
import shutil
import re
import sys
import subprocess

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
    
    ocr.addAction(uploadOcr)
    ocr.addAction(findOcr)
    
    self.addMenu(file)
    self.addMenu(ocr)
    
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
      target = open('tesseract.txt', 'r').read()
      target = re.sub('tesseract.exe', 'tessdata', target)
      shutil.copy(filePath, target)
        
  def openOcrWebpage(self):
    webbrowser.open('https://github.com/tesseract-ocr/tessdata')