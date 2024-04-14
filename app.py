from flask import Flask, flash,render_template, request, redirect, url_for, send_from_directory
import os
from OCR import text_extraction
from OCR import run_craft
import pandas as pd
from werkzeug.utils import secure_filename
import shutil
from create_folders import create_folders
from reset_exports import delete_files_in_directory
import shutil


create_folders()

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXPORT_FOLDER'] = EXPORT_FOLDER
base_path = os.path.dirname(__file__)

@app.route('/')
def index():
    return render_template('index_1_1.html')



@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(base_path, filename, as_attachment=True)



@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:

        filename = secure_filename(file.filename)
        filename_original = filename

        test_folder = 'test'
        filename = os.path.join(base_path + "/" + app.config['UPLOAD_FOLDER'], filename)

        print(filename)

        file.save(filename)
        images = os.listdir(app.config['UPLOAD_FOLDER'])

        for image in images:
            print(image, filename_original)
            if image == filename_original:
                shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], image), os.path.join(test_folder, image))

        run_craft()

        delete_files_in_directory("test")
        delete_files_in_directory('result')
        delete_files_in_directory('tets_boxes_from_craft/coords')
        delete_files_in_directory('tets_boxes_from_craft/imgs')

        with open('text_output.txt', 'r') as file:
            lines = file.readlines()

        txt_output = [line.strip() for line in lines]
        txt_output = [line for line in txt_output if line]


        with open('text_output.txt', 'w') as file:
            file.write(" ")


        if len(txt_output):

            extarcted_text,product_text = text_extraction(txt_output) # dict
            general_info = pd.DataFrame(extarcted_text)
            product_info = pd.DataFrame(product_text)

            print(filename_original)

            general_info["Image Name"] = filename_original

            with open('exports/number.txt', 'r') as file:
                number = file.read()

            number = int(number)

            output_path = os.path.join(base_path, f'exports/output{number}.xlsx') # whats with the path?

            # Writing general_info to the Excel file
            with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
                general_info.to_excel(writer, sheet_name='general_info', index=False)
                # Using index=False to exclude row numbers in the output

            # Appending product_info to the existing Excel file
            with pd.ExcelWriter(output_path, engine='openpyxl', mode='a') as writer:
                product_info.to_excel(writer, sheet_name='product_info', index=False)

            with open('exports/number.txt', 'w') as file:
                file.write(f'{number+1}')



            final_path = os.path.join(base_path, 'output.xlsx')

            print(final_path)

            shutil.copy(output_path, final_path)

            return render_template('result_1_1.html', output_path=final_path, os=os)

        else:
            print(filename_original)
            return render_template('result_2_2.html', image_filename=filename_original)


if __name__ == '__main__':
    try:
        print("!")
        app.run(debug=True)
        print("\n!")
    except Exception as e:
        print("Exp")
        exit(0)
    finally:
        print("!"+'TAGIL'*100)


