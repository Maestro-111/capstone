import os


"""
Run this file when you need to reset the image id for unit testing collection. 
It will reset the image num in exports, used to label each output table, to 0
"""


def delete_files_in_directory(directory_path):
    files = os.listdir(directory_path)
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    print("All files deleted successfully.")

if __name__ == '__main__':

    delete_files_in_directory("exports")

    with open('exports/number.txt', 'w') as file:
        file.write(f'{0}')

