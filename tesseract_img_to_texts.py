import cv2
import pytesseract
from pytesseract import Output
import pickle
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"
from os import listdir
from os.path import isfile, join
mypath = './downloads'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(files)
output = {}
for fi,f in enumerate(files):
    print(f, str(fi)+'/'+str(len(files)))
    if any([f.endswith(x) for x in ['.jpg', '.png']]):
        img = cv2.imread(join(mypath, f))

        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        texts=[]
        for i in range(len(d['text'])):
            if int(d['conf'][i]) > 25 and len(d['text'][i]) > 0:
                texts.append(d['text'][i])
        output[f[:-4]] = texts
    if fi%100==99:
        pickle.dump(output, open("pickle/texts.pkl", "wb"))
print(output)
pickle.dump(output, open("pickle/texts.pkl", "wb"))