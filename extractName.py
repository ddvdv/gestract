#! python3
# try and extact content of all kind of files with textract

import os, re, shutil, logging, subprocess #import for renaming

# Regex Formulas
regNumPV = re.compile('([0-9]{6})\/(20[0-9]{2})')
regNotice = re.compile('BR\.[0-9oz]{2}\.[0-9a-zA-Z]{2}\.[0-9oz]*\/2[0-9oz]{3}')
regDate = re.compile('([0-3][0-9])-([0-1][0-9])-(20[0-3][0-9])')
regObject = re.compile('([oO]bjet)(.*)?(Fait)')

# Absolue path to foler
absPathFolder = os.path.abspath('./confi')
for root, dirs, files in os.walk(absPathFolder):
    for fileName in files:
        if fileName.endswith('test.pdf'):
            print('current file: ' + fileName)

            # OCR if no text
            absPathFile = os.path.join(root, fileName)

            # Extract text 1st page with pdfreader
            #cmd = ["pdftotext", '-x 200', '-y 400', '-W 600', '-H 50', absPathFile]
            cmd = ["pdf2txt", absPathFile]
            print(cmd)
            logging.debug(cmd)
            proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            text1 = str(proc.stdout.read())
            #print("first page:")
            print(text1)

            if hasattr(regObject.search(text1), "group"):
                resultObject = regObject.search(text1)
                resultGroup = resultObject.group(2)
                print("this is the object")
                print(resultGroup)
