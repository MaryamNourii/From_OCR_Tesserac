import os
import re
from PIL import Image
from pytesseract import image_to_string
import csv


def read_words_csv(input_folder, csv_file):
    data = {}
    with open(os.path.join(input_folder, csv_file) , 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        # next(reader, None) 
        for row in reader:
            img = row[0]
            x = row[1]
            y = row[2]
            w = row[3]        
            h = row[4]        
            data[img] = [img,x,y,w,h]
    return data


def is_image( file):
    return re.match(r".*\.(jpg|jpeg|png|bmp|tif|tiff)$", file, re.IGNORECASE)


def ocr_process(input_folder, data):
    # header = ['name','x', 'y', 'w', 'h','prd']
    output_file = 'ocr_result.csv'
    config = '-c preserve_interword_spaces=5 --psm 6 --oem 1 -l fas+ara tessedit_char_whitelist="آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی ۰١۲۳۴٤۵٥۶٦۷۸۹.,،:/"'
    with open(output_file, "w", encoding='utf8', newline="") as out_file:
        writer = csv.writer(out_file)
        # writer.writerow(header)    
        for file in os.listdir(input_folder):
            if is_image(file):
                file_path = os.path.join(input_folder, file)
                image = Image.open(file_path)
                text = image_to_string(image, config=config)
                ind = file.split('.')[0]
                writer.writerow([ind, data[ind][1], data[ind][2], data[ind][3], data[ind][4], text.strip()])

    print("OCR has been performed on all images in the folder.")


def main(input_folder = '..//words', csv_file = 'words.csv'):
    os.environ["TESSDATA_PREFIX"] = 'C://Program Files//Tesseract-OCR//tessdata' 
    data = read_words_csv(input_folder, csv_file)
    ocr_process(input_folder, data)

if __name__ == "__main__":
    main()
