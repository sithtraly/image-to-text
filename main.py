import sys
import shutil
import os
import pytesseract
from PyQt5.QtWidgets import (
  QApplication, QWidget, QLabel, QPushButton, QTextEdit,
  QVBoxLayout, QFileDialog, QMessageBox, QComboBox, 
)
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image

class App(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowIcon(QIcon("icon.png"))
    self.lastPath = os.path.expanduser("~")
    self.setWindowTitle('Image to Text (OCR)')
    self.setGeometry(100, 100, 800, 600)
    self.setAcceptDrops(True)
    
    # Widgets
    self.imageLabel = QLabel('No image loaded')
    self.imageLabel.setScaledContents(True)
    self.imageLabel.setMaximumHeight(300)
    
    self.textOutput = QTextEdit()
    self.textOutput.setPlaceholderText('Extracted text will appear here.')
    self.textOutput.setReadOnly(True)
    
    self.loadButton = QPushButton('Load Image')
    self.convertButton = QPushButton('Convert')
    
    self.langSelector = QComboBox()
    
    # Layout
    layout = QVBoxLayout()
    layout.addWidget(self.loadButton)
    layout.addWidget(self.langSelector)
    layout.addWidget(self.convertButton)
    layout.addWidget(self.imageLabel)
    layout.addWidget(self.textOutput)
    self.setLayout(layout)
    
    # Event
    self.loadButton.clicked.connect(self.loadImage)
    self.convertButton.clicked.connect(self.convert)
    
    self.imagePath = None
  
  def dragEnterEvent(self, e):
    if e.mimeData().hasUrls():
      e.acceptProposedAction()
    else:
      e.ignore()
      
  def dropEvent(self, e):
    urls = e.mimeData().urls()
    if urls:
      self.imagePath = urls[0].toLocalFile()
      self.imageLabel.setPixmap(QPixmap(self.imagePath))
    
  def loadImage(self):
    fileName, _ = QFileDialog.getOpenFileName(
      self, 'Open image', self.lastPath, 'Image Files (*.png *.jpeg *.jpg *.bmp)'
    )
    
    if fileName:
      self.imagePath = fileName
      self.imageLabel.setPixmap(QPixmap(fileName))
      self.lastPath = os.path.dirname(fileName)
  
  def convert(self):
    if not self.imagePath:
      self.textOutput.setPlainText('Please load image first!')
      return
    
    # OCR Process
    image = Image.open(self.imagePath)
    lang = self.langSelector.currentText()
    text = pytesseract.image_to_string(image, lang=lang)
    self.textOutput.setPlainText(text)
  
def checkTessract(self):
  if shutil.which("tesseract"):
    print("✅ Tesseract is installed and in PATH.")
  else:
    file_path = None
    if os.path.exists('tesseract.txt'):
      f = open('tesseract.txt', 'r')
      file_path = f.read(file_path)
    if not file_path:
      file_path, _ = QFileDialog.getOpenFileName(
        self,
        "Locate tesseract.exe",
        "",
        "Executable Files (*.exe)"  # Only show .exe on Windows
      )
    
    if file_path:
      # Test if it's a working tesseract
      import subprocess
      try:
        result = subprocess.run([file_path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
          # Save this path and set it for pytesseract
          import pytesseract
          pytesseract.pytesseract.tesseract_cmd = file_path
          f = open('tesseract.txt', 'w')
          f.write(file_path)
          if not os.path.exists('tesseract.txt'):
            QMessageBox.information(self, "Success", "Tesseract path set successfully!")
        else:
          QMessageBox.warning(self, "Error", "The selected file is not a valid Tesseract executable.")
      except Exception as e:
        QMessageBox.critical(self, "Error", f"Failed to run Tesseract:\n{str(e)}")  

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = App()
  checkTessract(window)
  window.show()
  langs = pytesseract.get_languages(config='')
  window.langSelector.addItems(langs)
  window.langSelector.setCurrentText(langs[0])
  sys.exit(app.exec())