import os
import pytesseract
from PyQt5.QtWidgets import (
  QWidget, QLabel, QPushButton, QTextEdit,
  QVBoxLayout, QFileDialog, QComboBox, QGridLayout,
  QSizePolicy, QMainWindow, QApplication, QShortcut
)
from PyQt5.QtCore import QSettings, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence, QFont, QFontDatabase
from PIL import Image, ImageQt
import PIL
import re

from components.menu import MenuBar

PIL.ImageQt.QBuffer = QBuffer
PIL.ImageQt.QIODevice = QIODevice

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    fontPath = os.path.join('fonts', 'NotoSansKhmer-Regular.ttf')
    fontId = QFontDatabase.addApplicationFont(fontPath)
    if fontId == -1:
      print("Failed to load font!")
    else:
      print(fontId)

    NotoSansKhmer = QFontDatabase.applicationFontFamilies(fontId)[0]
    self.font = QFont(NotoSansKhmer, 12)

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
    # self.imageLabel.setMaximumHeight(300)
    # self.imageLabel.setMaximumWidth(300)
    
    self.textOutput = QTextEdit()
    self.textOutput.setPlaceholderText('Extracted text will appear here.')
    self.textOutput.setReadOnly(True)
    self.textOutput.setFont(self.font)
    
    self.loadButton = QPushButton('Load Image')
    self.convertButton = QPushButton('Convert')
    self.pasteButton = QPushButton('Paste from clipboard')
    
    self.langSelector = QComboBox()
    
    # Button layout
    btLayout = QGridLayout()
    btLayout.setVerticalSpacing(10)
    btPerRow = 4
    for i, bt in enumerate([self.pasteButton, self.loadButton, self.langSelector, self.convertButton]):
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
    self.pasteButton.clicked.connect(self.pasteFromClipboard)
    
    self.imagePath = None

    paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
    paste_shortcut.activated.connect(self.pasteFromClipboard)
    
    # menu.menuBar(self)
  
  def pasteFromClipboard(self):
    clipboard = QApplication.clipboard()
    image = clipboard.image()

    if not image.isNull():
      pixmap = QPixmap.fromImage(image)
      self.imageLabel.setPixmap(pixmap)
  
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
    if self.imagePath:
      # OCR Process
      image = Image.open(self.imagePath)
    elif self.imageLabel.pixmap() is not None:
      qimage = self.imageLabel.pixmap().toImage()
      image = ImageQt.fromqimage(qimage)
    else:
      self.textOutput.setPlainText('Please load image first!')
      return
    
    lang = self.langSelector.currentText()
    text = pytesseract.image_to_string(image, config=f'-l eng+{lang}')
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    self.textOutput.setPlainText(text)