import os

def create_folder_if_not_exists(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # If the folder doesn't exist, create it
        os.makedirs(folder_path)
        print(f"Folder created: {folder_path}")
    else:
        print(f"Folder already exists: {folder_path}")


def create_folders():

    create_folder_if_not_exists("tets_boxes_from_craft/coords")
    create_folder_if_not_exists("tets_boxes_from_craft/imgs")
    create_folder_if_not_exists("uploads")
    create_folder_if_not_exists("exports")
    create_folder_if_not_exists("test")
    create_folder_if_not_exists("result")
    create_folder_if_not_exists("contours")

    with open('exports/number.txt', 'w') as file:
        file.write(f'{0}')
