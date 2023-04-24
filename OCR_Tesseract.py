import os
import re
from PIL import Image
from pytesseract import image_to_string
import csv

class OCR_Tesseract():
    def __init__(self, input_folder, csv_file):
        self.input_folder = input_folder
        self.csv_file = csv_file
        os.environ["TESSDATA_PREFIX"] = 'C:\\Program Files\\Tesseract-OCR\\tessdata' 
    
    def read_words_csv(self):
        data = {}
        with open(os.path(self.input_folder, self.csv_file) , 'r', encoding='utf8') as file:
            reader = csv.reader(file)
            # next(reader, None) 
            for row in reader:
                img = row[0]
                x = row[1]
                y = row[2]
                w = row[3]        
                h = row[4]        
                self.data[img] = [img,x,y,w,h]

    def is_image(self, file):
        return re.match(r".*\.(jpg|jpeg|png|bmp|tif|tiff)$", file, re.IGNORECASE)
    
    def ocr_process(self):
        # header = ['name','x', 'y', 'w', 'h','prd']
        output_file = 'ocr_result.csv'
        config = '-c preserve_interword_spaces=5 --psm 6 --oem 1 -l fas+ara tessedit_char_whitelist="آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی ۰١۲۳۴٤۵٥۶٦۷۸۹.,،:/"'
        with open(output_file, "w", encoding='utf8') as out_file:
            writer = csv.writer(out_file)
            # writer.writerow(header)    
            for file in os.listdir(self.input_folder):
                if self.is_image(file):
                    file_path = os.path.join(self.input_folder, file)
                    image = Image.open(file_path)
                    text = image_to_string(image, config=config)
                    ind = file.split('.')[0]
                    writer.writerow([ind, self.data[ind][1], self.data[ind][2], self.data[ind][3], self.data[ind][4], text.strip()])

        print("OCR has been performed on all images in the folder.")

 

