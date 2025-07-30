import sys
import shutil
import os
import pytesseract
from PyQt5.QtWidgets import (
  QApplication, QFileDialog, QMessageBox,
)

from components.mainwindows import MainWindow
  
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
  window = MainWindow()
  checkTessract(window)
  window.show()
  langs = pytesseract.get_languages(config='')
  window.langSelector.addItems(langs)
  window.langSelector.setCurrentText(langs[0])
  sys.exit(app.exec())