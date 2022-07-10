import cv2
import numpy as np
import pytesseract


def read_img(receipt_file):
    img = cv2.imread('D:\\Github\\Cost-Splitting-HEAP\\pyTesseract_test\\IMG_1636.jpeg',0) # change to variable when this is converted into a function // 0 = greyscale 

    custom_config = r'--oem 3 --psm 6'
    output = pytesseract.image_to_data(img, config=custom_config, output_type='dict')
    true_output = output['text']
    #placing everything into an array
    placeholder = []
    temp = ''
    for item in true_output:
        if item == '':
            if temp != '':
                placeholder.append(temp)
                temp = ''
        else:
            if temp == '':
                temp += item
            else:
                temp += " " + item

    # print(placeholder)
    #since main total is always at the back, therefore run the array from the back to find the first instance of total
    #haven think of formatting of receipts yet as some receipts has huge spacing between total and value
    placeholder.reverse()
    finder = False
    num = 0
    total = ''
    while(not finder):
        tempp = placeholder[num].lower()
        tempp = tempp.split()
        if ('total' in tempp or "total:" in tempp) and len(tempp) <= 3:
            finder = True
            total = placeholder[num]
        num += 1
    output_dict = {'Total': 0.0}
    temppp = ''
    for char in total:
        if char.isnumeric() or char == '.':
            temppp += char
        elif char.lower() in 'total' and temppp != '':
            temppp = ''
    output_dict['Total'] = float(temppp)
    # to be returned as a dict variable {string : float}
    # print(output_dict)
    
    return output_dict


