import os
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QLabel, QPushButton, QGridLayout
from functools import partial

from components.myfunc import getLangs, getPath

class OcrListDialog(QDialog):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("OCR List")
    self.layout = QVBoxLayout()
    self.loadData()

    self.setLayout(self.layout)

  def loadData(self):
    langs = getLangs()
    for i, lang in enumerate(langs):
      label = QLabel(f'{lang}.traineddata', self)
      button = QPushButton('Remove')
      button.clicked.connect(partial(self.remove, lang))
      gridLayout = QGridLayout()
      gridLayout.addWidget(label, 1, 1)
      gridLayout.addWidget(button, 1, 2)
      self.layout.addLayout(gridLayout)
  
  def remove(self, lang):
    ocrPath = getPath(os.path.join('Tesseract-OCR', 'tessdata'))
    langPath = os.path.join(ocrPath, f'{lang}.traineddata')
    if os.path.exists(langPath):
      os.remove(langPath)
      self.close()
      dlg = OcrListDialog()
      dlg.exec_()
    print(lang)
