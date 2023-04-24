import cv2
import os
import numpy as np
import csv

class preprocessing():
    def __init__(self, path):
        self.path = path

    def read_img(self):
        self.img = cv2.imread(self.path)

    def enhancing_image(self):
        image = self.img.copy()

        height =image.shape[0]
        width = image.shape[1]

        w =int(image.shape[0] * 8)
        h =int(image.shape[1] * 8)
        image = cv2.resize(image, (w, h),interpolation=cv2.INTER_CUBIC)                                                                                                                                                                                                                                                                                                                       

        mask = np.zeros(image.shape, dtype=np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 10000:
                cv2.drawContours(mask, [c], -1, (255,255,255), -1)

        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        result = cv2.bitwise_and(image,image,mask=mask)
        result[mask==0] = (255,255,255)

        self.enhanced_img = cv2.resize(result, (width, height),interpolation=cv2.INTER_CUBIC)
        cv2.imshow(self.enhanced_img)

    def detect_word(self, img):
        word_count = 0
        pos = []
        image = self.enhanced_img .copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.blur(gray, (15, 12))
        thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # cv2.imshow(thresh)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if (x == 0):  x+=5
            if (y == 0):  y+=5
            if ([x,y,w,h] not in pos and w > 0 and h > 0) : 
                cv2.rectangle(image, (x-5, y-5), (x+w+5, y+h+5), (0, 255, 0), 2)
                word = image[y-5:y+h+5, x-5:x+w+5]
                word_pos=[x, y, w, h]
                pos.append([x, y, w, h])
                self.words[word_count]={'img' : word,'pos':word_pos}
                word_count += 1
        cv2.imshow(image)

    def save_words(self):
        # header = ['name','x', 'y', 'w', 'h']
        with open('words//words.csv', 'w') as file:
            writer = csv.writer(file)
            # writer.writerow(header)
            for i, (key , values) in enumerate(self.words.items()):
                writer.writerow([str(key), str(values['pos'][0]), str(values['pos'][1]) ,  str(values['pos'][2]) , str(values['pos'][3])])
                cv2.imwrite('words/' + str(key)  + '.png', values['img'])
