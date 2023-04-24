import Preprocess
import OCR_Tesseract
import csv
import os
import cv2

data = {}

def read_results():
    with open('ocr_result.csv', 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        for row in reader:
            img = row[0]
            x = row[1]
            y = row[2]
            w = row[3]        
            h = row[4]        
            prd = row[5]        
            data[img] = [img,x,y,w,h,prd]

def show_results():
    data_dir = 'words'
    words=[]
    for item in os.listdir(data_dir):
        img = cv2.imread(os.path.join(data_dir,item))
        if img is not None:
            words.append(img)
            print('pred------' + data[item.split('.')[0]][5])
            cv2.imshow(img)            
            cv2.waitKey()


def main():
    Preprocess.main('imges//F2.jpg')
    OCR_Tesseract.main('words', 'words.csv')
    read_results()
    show_results()


if __name__ == "__main__":
    main()
