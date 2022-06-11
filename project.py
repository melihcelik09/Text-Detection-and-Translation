import cv2
import pytesseract
import imutils
from tkinter import *
import tkinter.font as tkFont
from tkinter import filedialog as fd
from translate import Translator

sentences_list = []
translated_list = []
def take_photo():
    cap = cv2.VideoCapture(0)
    while True:
        ret,frame=cap.read()
        if ret==True:
            cv2.imshow('Take Photo',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite('target.png',frame)
                break
    cap.release()
    cv2.destroyAllWindows()
def select_photo():
        global img,text_img,translate_img
        filepath = fd.askopenfilename(title='Select Image')
        print("Filepath: " + filepath)
        img = cv2.imread(filepath)
        img=imutils.resize(img,width=500)
        text_img=img.copy()
        translate_img=img.copy()
def ocr_image():
    try:
        data=pytesseract.image_to_data(img)
        for z,a in enumerate(data.splitlines()):
                if z!=0:
                    a=a.split()
                    if(len(a)==12):
                        x,y,w,h=int(a[6]),int(a[7]),int(a[8]),int(a[9])
                        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow('Image To OCR',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        print("No image selected")
def image2text():
    try:
        config=r'-l eng+tur --oem 3 --psm 6'
        text = pytesseract.image_to_string(text_img,config=config)
        print(text)
        if len(sentences_list)==0:
            sentences_list.append(text)
            print("Sentences added to list")

    except:
        print("No image selected")
def text2translate():
    if len(sentences_list) == 0:
        print("No text to translate")
    else:
        translator = Translator(to_lang="tr")
        for sentence in sentences_list:
            try:
                if len(translated_list)==0:
                    translated = translator.translate(sentence)
                    translated_list.append(translated)
                    print("Translated text added to list")
            except:
                print("Error")
        if len(translated_list)>0:
            print("Translated all sentences")
            # file=open("translated.txt","w")
            # file.write(str(translated_list))
            # file.close()
            for sentence in translated_list:
                print(sentence)
root=Tk()
root.title('Image to Translate')
root.geometry('300x400')
fontSettings = tkFont.Font(family='Helvetica',weight='bold')
pane=Frame(root)
pane.pack(fill=BOTH,expand=True)
Button(pane,text='Take Photo',command=take_photo,font=fontSettings).pack(fill=BOTH,expand=True)
Button(pane,text='Select Photo',command=select_photo,font=fontSettings).pack(fill=BOTH,expand=True)
Button(pane,text='OCR',command=ocr_image,font=fontSettings).pack(fill=BOTH,expand=True)
Button(pane,text='Text',command=image2text,font=fontSettings).pack(fill=BOTH,expand=True)
Button(pane,text='Translated',command=text2translate,font=fontSettings).pack(fill=BOTH,expand=True)
Button(pane,text='Exit',command=root.destroy,font=fontSettings).pack(fill=BOTH,expand=True)
root.mainloop()
