# OCR with Flask Web App


## Abstract
In this project the aim is to extract text information from receipts images. 
The application is wrapped into a simple Flaks app.

<img width="1000" alt="teaser" src="./figure/image_schema.PNG">


## Prerequisites

1. You have to install our Custom_CRAFT package to run the code. This is a modification of original CRAFT package. Note that you have to install Python 3.9 or lower to run CRAFT.
2. You have to establish your Open AI key to use GPT API.


## How to run

1. Make sure you have installed our modified CRAFT package (link is below)
2. Create venv with this directory
3. activate venv
4. Install the requirements from requirements.txt
5. From terminal run flask app with 'flask run' command.
6. Upload any photo from sample data folder to the website. 
7. wait and download the resulting Excel file


## Methodology
1. Text Region Identification: CRAFT package is used to get the ROI's in the image.
2. Text Extraction: EasyOCR is used for text extraction.
3. Text Analysis with LLM: GPT-4 is used to extract text information from OCR data.
   
Links:
- Original CRAFT: [Link](https://github.com/clovaai/CRAFT-pytorch)
- Custom CRAFT: [Link](https://github.com/Maestro-111/Custom-Craft.git)
- EasyOCR: [Link](https://github.com/JaidedAI/EasyOCR)


## Evaluations

Each time user upload their photo, program stores the resulting table in a folder. 
unit testing.py merges all the outputs into one table and compares it with database.xlsx to log out the errors.


- Evaluation Metrics: Accuracy via using unit testing.py.
- Limitations: Dependency on image quality. Also, the web app is not publicly available.

## Unit testing

- For Unit testing: Each time you run the program, it stores the output table for each receipt in exports folder.
- Unit testing.py merges all outputs into one table and compares with database.xlsx. In order to refresh the exports folder you can run reset_exports.py


## TO DO

1. Work on GPT prompt. Not accurate in identifying address.



