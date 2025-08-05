import os
import sys
import pytesseract

def getPath(relativePath):
  if hasattr(sys, '_MEIPASS'):
    return os.path.join(sys._MEIPASS, relativePath)
  return os.path.abspath(relativePath)

def getLangs():
  langs = pytesseract.get_languages()
  return langs