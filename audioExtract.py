#! python3
# try and extact content of all kind of files with textract

import logging, subprocess, sys  #import for OCR
import os, re, shutil, textract  #import for renaming

filename = "Carte.ogg"
absPathFile = os.path.abspath(filename)
text = str(textract.process(absPathFile))
print(text)
