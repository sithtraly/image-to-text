from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt5.QtCore import Qt

from version import __version__

class AboutDialog(QDialog):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("About")

    self.labelVersion = QLabel(f'Version: {__version__}', self)
    self.labelAuthor = QLabel('Author: Traly', self)
    self.labelLanguage = QLabel('Language: Python', self)
    self.labelLib = QLabel('Library: Tesseract', self)

    self.buttons = QDialogButtonBox.Cancel
    self.buttonBox =  QDialogButtonBox(self.buttons)

    self.buttonBox.rejected.connect(self.reject)
    self.buttonBox.button(QDialogButtonBox.Cancel).setText('Close')

    layout = QVBoxLayout()
    layout.addWidget(self.labelVersion, alignment=Qt.AlignCenter)
    layout.addWidget(self.labelAuthor, alignment=Qt.AlignCenter)
    layout.addWidget(self.labelLanguage, alignment=Qt.AlignCenter)
    layout.addWidget(self.labelLib, alignment=Qt.AlignCenter)
    layout.addWidget(self.buttonBox)
    self.setLayout(layout)
