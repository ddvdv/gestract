#! python3
# try and extact content of all kind of files with textract

import os, re, shutil, textract

# Regex Formulas
regNumPV = re.compile('([0-9]{6})\/(20[0-9]{2})')
regNotice = re.compile('BR\.[0-9oz]{2}\.[0-9a-zA-Z]{2}\.[0-9oz]*\/2[0-9oz]{3}')
regDate = re.compile('([0-3][0-9])-([0-1][0-9])-(20[0-3][0-9])')
regObject = re.compile('(Objet du PV)(.*)(\\n)?')
regEscape = re.compile('\/')

# Absolue path to foler
absPathFolder = os.path.abspath('./PVx')
for root, dirs, files in os.walk(absPathFolder):
    for fileName in files:
        print('this is a file: ' + fileName)
        if fileName.endswith('.pdf'):
            absPathFile = os.path.join(root, fileName)
            text = str(textract.process(absPathFile))
            resultPV = regNumPV.search(text).group()
            resultNumPV = regNumPV.search(text).group(1)
            resultRegPV = regNumPV.search(text).group(2)
            resultNumNotice = regNotice.search(text).group()
            resultObject = regObject.search(text).group()
            resultDate = regDate.search(text).group()
            resultYear = regDate.search(text).group(3)
            resultMonth = regDate.search(text).group(2)
            resultDay = regDate.search(text).group(1)
            print(resultNumPV)
            print(resultNumNotice)
            #print(resultObject.group(2))
            print(resultDate)
            #print(str(text))
            print(text)
            newName = resultYear + resultMonth + resultDay + '_PV_' + resultNumPV + '.pdf'
            newName = regEscape.sub('--', newName)
            newNamePath = os.path.join(root, newName)
            shutil.copy(absPathFile, newName)
