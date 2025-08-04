import os
import sys
import pytesseract

def getPath(relativePath):
  if hasattr(sys, '_MEIPASS'):
    return os.path.join(sys._MEIPASS, relativePath)
  return os.path.abspath(relativePath)

def reloadLangs(self):
  langs  = pytesseract.get_languages()
  for lang in langs:
    if (len(self.langs)) <= 0:
      self.langs += lang
    else:   
      self.langs += f'+{lang}'
  print(langs)