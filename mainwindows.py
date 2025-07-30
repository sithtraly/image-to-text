import os
import pytesseract
from PyQt5.QtWidgets import (
  QWidget, QLabel, QPushButton, QTextEdit,
  QVBoxLayout, QFileDialog, QComboBox, QGridLayout,
  QSizePolicy, QMainWindow,
)
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image
import re

from menu import MenuBar

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setting = QSettings('ImageToText', 'ImageToText')
    menuBar = MenuBar(self)
    self.setMenuBar(menuBar)
    
    centralWidget = QWidget()
    self.setCentralWidget(centralWidget)
    
    self.setWindowIcon(QIcon("icon.ico"))
    self.lastPath = os.path.expanduser("~")
    self.setWindowTitle('Image to Text (OCR)')
    self.setGeometry(100, 100, 800, 600)
    self.setAcceptDrops(True)
    
    # Widgets
    self.imageLabel = QLabel('No image loaded')
    self.imageLabel.setScaledContents(True)
    self.imageLabel.setMaximumHeight(300)
    self.imageLabel.setMaximumWidth(300)
    
    self.textOutput = QTextEdit()
    self.textOutput.setPlaceholderText('Extracted text will appear here.')
    self.textOutput.setReadOnly(True)
    
    self.loadButton = QPushButton('Load Image')
    self.convertButton = QPushButton('Convert')
    
    self.langSelector = QComboBox()
    
    # Button layout
    btLayout = QGridLayout()
    btLayout.setVerticalSpacing(10)
    btPerRow = 3
    for i, bt in enumerate([self.loadButton, self.langSelector, self.convertButton]):
      row = i // btPerRow
      col = i % btPerRow
      bt.setFixedHeight(30)
      bt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
      btLayout.addWidget(bt, row, col)
    
    layout = QVBoxLayout()
    layout.addLayout(btLayout)
    layout.addWidget(self.imageLabel)
    layout.addWidget(self.textOutput)
    centralWidget.setLayout(layout)
    
    # Event
    self.loadButton.clicked.connect(self.loadImage)
    self.convertButton.clicked.connect(self.convert)
    
    self.imagePath = None
    
    # menu.menuBar(self)
  
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
      self, 'Open image', self.setting.value('lastPath', '~'), 'Image Files (*.png *.jpeg *.jpg *.bmp)'
    )
    
    if fileName:
      self.imagePath = fileName
      self.imageLabel.setPixmap(QPixmap(fileName))
      self.setting.setValue('lastPath', os.path.dirname(fileName))
  
  def convert(self):
    if not self.imagePath:
      self.textOutput.setPlainText('Please load image first!')
      return
    
    # OCR Process
    image = Image.open(self.imagePath)
    lang = self.langSelector.currentText()
    text = pytesseract.image_to_string(image, lang=lang)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    self.textOutput.setPlainText(text)
    # print(self.textOutput.toPlainText())