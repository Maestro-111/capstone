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



def run_craft():
    anaconda_python_path = r'C:/Python39/python.exe'
    command = [anaconda_python_path, "C:/Custom-Craft/test.py", "--trained_model", "craft_mlt_25k.pth", "--test_folder", "test/"]
    subprocess.run(command)

def text_extraction(text):

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    with open('prompt.txt', 'r') as file:
        message_template = file.read()

    message = message_template.format(text)

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
    resp = resp.split('\n')

    resp = [i for i in resp if i]


    total = None
    subtotal = None
    name_of_store = None
    pay_type = None
    date = None # 4
    address = None # 5
    products = [] # 6
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
        elif i == 4:
            date = value
        elif i == 5:
            address = value
        else:
            value = value.split(',')

            count = 1

            for i in range(len(value)):
                dumb_names.append(f"product#{count}")
                count += 1


            products = value

    data1 = {'total': [total], 'subtotal': [subtotal], 'store': [name_of_store], 'payment type': [pay_type], 'date':[date],'address':[address]}

    data2 = {'product_count':dumb_names, 'product_name':products}

    return data1,data2



