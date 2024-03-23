import cv2
import pytesseract
import pandas as pd
from matplotlib import pyplot as plt
import re
import numpy as np
import subprocess

import openai
from openai import OpenAI
import os

def is_contour_inside(contour1, contour2,eps=5): # check if contour1 in contour2; eps - allow small deviation
    x1, y1, w1, h1 = cv2.boundingRect(contour1)
    x2, y2, w2, h2 = cv2.boundingRect(contour2)

    return x2 <= x1+eps and y2 <= y1 + eps and x2 + w2 + eps >= x1 + w1 and y2 + h2 + eps >= y1 + h1

def remove_contours_inside(contours):
    filtered_contours = []

    # Iterate through each contour
    for i in range(len(contours)):
        is_inside = False

        # Compare with other contours
        for j in range(len(contours)):
            if i != j and is_contour_inside(contours[i], contours[j]):
                is_inside = True
                break

        # If the contour is not inside any other, add it to the result
        if not is_inside:
            filtered_contours.append(contours[i])

    return filtered_contours

def write_list_of_lists_to_file(list_of_lists, file_name):
    with open(file_name, 'w') as f:
        for inner_list in list_of_lists:
            f.write(' '.join(map(str, inner_list)) + '\n')

def run_OCR_analysis(image_path):

    image = cv2.imread(image_path)

    plt.imshow(image)
    plt.show()

    k = 3
    threshold_percentage = 0.8
    threshold_value = 160


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    for i in range(len(gray)):
        for j in range(len(gray[0])):
            if gray[i][j] < threshold_value:
                gray[i][j] = 0

    plt.imshow(gray)
    plt.show()

    for i in range(len(gray)):
        for j in range(len(gray[0])):

            if gray[i][j] != 0:

                vert_pos_n = []
                vert_neg_n = []
                horizont_neg_j = []
                horizont_pos_j = []

                copy_i = i
                count = 0
                while copy_i + 1 < len(gray) and count < k:
                    vert_pos_n.append(gray[copy_i + 1][j])
                    copy_i += 1
                    count += 1

                copy_i = i
                count = 0
                while copy_i - 1 >= 0 and count < k:
                    vert_pos_n.append(gray[copy_i - 1][j])
                    copy_i -= 1
                    count += 1

                copy_j = j
                count = 0
                while copy_j + 1 < len(gray[0]) and count < k:
                    horizont_pos_j.append(gray[i][copy_j + 1])
                    copy_j += 1
                    count += 1

                copy_j = j
                count = 0
                while copy_j - 1 >= 0 and count < k:
                    horizont_neg_j.append(gray[i][copy_j - 1])
                    copy_j -= 1
                    count += 1

                # Count zeros in neighbors
                zero_count = sum(pixel == 0 for pixel in vert_pos_n + vert_neg_n + horizont_neg_j + horizont_pos_j)

                # Check if 80% or more of the neighbors are zero
                if zero_count >= threshold_percentage * len(vert_pos_n + vert_neg_n + horizont_neg_j + horizont_pos_j):
                    gray[i][j] = 0


    write_list_of_lists_to_file(gray,'coords.txt')

    edged = cv2.Canny(gray, 40, 250)

    plt.imshow(edged)
    plt.show()

    cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = remove_contours_inside(cnts)

    points = []
    for cnt in cnts:
        points += [pt[0] for pt in cnt]

    points_array = np.array(points).reshape(-1, 1, 2)
    hull = cv2.convexHull(points_array)

    hull_cnts = cv2.drawContours(image.copy(), [hull], -1, (0, 255, 0), 3)
    plt.imshow(hull_cnts)
    plt.show()

    x, y, w, h = cv2.boundingRect(hull)

    roi = image[y:y + h, x:x + w]

    new_width = 3 * roi.shape[1]  # Increase width by a factor of 2
    new_height = 3 * roi.shape[0]  # Increase height by a factor of 2
    resized_roi = cv2.resize(roi, (new_width, new_height))

    plt.imshow(resized_roi)
    plt.show()

    custom_config = r'--psm 4'
    text = pytesseract.image_to_string(resized_roi, config=custom_config)
    return text

def run_craft():
    anaconda_python_path = r'C:/Python39/python.exe'
    command = [anaconda_python_path, "C:/Custom-Craft/test.py", "--trained_model", "craft_mlt_25k.pth", "--test_folder", "test/"]
    subprocess.run(command)

def text_extraction(text):

    #print(text)

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    message = f"Given the following text extracted from receipt message: {text} , I want you to retrieve information in the strictly in the following format:" \
              f"total amount: derived total amount from the text" \
              f"subtotal amount: derived subtotal amount from the text" \
              f"Name of Store: derived Name of Store from the text" \
              f"Payment type: derived Payment type from the text" \
              f"List of the products found the in receipt, like this - list of products: product#1,product#2,product#3 and so on. make sure that the product list (products: product#1,product#2,product#3) is in one line"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-4",
    )

    resp = chat_completion.choices[0].message.content
    #print(resp)
    resp = resp.split('\n')
    #(resp)

    resp = [i for i in resp if i]


    total = None
    subtotal = None
    name_of_store = None
    pay_type = None
    products = []
    dumb_names = []

    for i in range(len(resp)):
        st = resp[i]

        try:
            name,value = st.split(":")
        except ValueError:
            continue

        if i == 0:
            total = value
        elif i == 1:
            subtotal = value
        elif i == 2:
            name_of_store = value
        elif i == 3:
            pay_type = value
        else:
            value = value.split(',')

            count = 1

            for i in range(len(value)):
                dumb_names.append(f"product#{count}")
                count += 1


            products = value

    data1 = {'total': [total], 'subtotal': [subtotal], 'store': [name_of_store], 'payment type': [pay_type]}

    data2 = {'product_count':dumb_names, 'product_name':products}

    return data1,data2



