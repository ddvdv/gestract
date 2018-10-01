#! python3
# try and extact content of all kind of files with textract

import logging, subprocess, sys   #import for OCR
import os, re, shutil, textract, PyPDF2  #import for renaming

# Regex Formulas
regNumPV = re.compile('([0-9]{6})\/(20[0-9]{2})')
regNotice = re.compile('BR\.[0-9oz]{2}\.[0-9a-zA-Z]{2}\.[0-9oz]*\/2[0-9oz]{3}')
regDate = re.compile('([0-3][0-9])-([0-1][0-9])-(20[0-3][0-9])')
regObject = re.compile('(Objet du PV)(\\n\\n..)')
regEscape = re.compile('\/')

# create folder if doesnt exist
if not os.path.exists('sorted'):
    os.makedirs('sorted')

# Absolue path to foler
absPathFolder = os.path.abspath('./confi')
for root, dirs, files in os.walk(absPathFolder):
    for fileName in files:
        print('this is a file: ' + fileName)
        if fileName.endswith('.pdf'):
            # OCR if no text
            absPathFile = os.path.join(root, fileName)
            absPathOcred = os.path.join(root, 'ocr_' + fileName)
            cmd = ["ocrmypdf",  "--deskew", absPathFile, absPathOcred]
            #print(cmd)
            #logging.debug(cmd)
            #proc = subprocess.Popen(
                #cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #result = proc.stdout.read()
            #if proc.returncode == 6:
                #print("Skipped document because it already contained text")
            #elif proc.returncode == 0:
                #print("OCR complete")
            #logging.debug(result)

            # Extract text with textract
            absPathFile = os.path.join(root, fileName)
            text = str(textract.process(absPathFile))

            # Extract text 1st page with pdfreader
            cmd = ["pdftotext", '-f 1 -l 1', absPathFile]
            logging.debug(cmd)
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            text1 = str(proc.stdout.read())
            #print(text1)

            if hasattr(regNumPV.search(text), "group"):
                resultNumPV = regNumPV.search(text).group(1)
                resultRegPV = regNumPV.search(text).group(2)
            if hasattr(regNotice.search(text), "group"):
                resultNumNotice = regNotice.search(text).group()
            if hasattr(regObject.search(text), "group"):
                pass
            #resultObject = regObject.search(text1).group(2)
            if hasattr(regDate.search(text), "group"):
                resultDate = regDate.search(text).group()
                resultYear = regDate.search(text).group(3)
                resultMonth = regDate.search(text).group(2)
                resultDay = regDate.search(text).group(1)
                newName = resultRegPV + '_' + resultNumPV + '_PV.pdf'
                newName = regEscape.sub('--', newName)
                #print('File named ' + fileName + ' will be renamed ' + newName)
                newNamePath = os.path.join('sorted', newName)
                shutil.copy(absPathFile, newNamePath)
                print(absPathFile, newName)
            else:
                shutil.copy(absPathFile, 'sorted/'+ fileName)
                print(absPathFile, 'sorted/'+ fileName)
