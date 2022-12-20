from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import shutil
from time import monotonic
from threading import Thread

# create a dictionary of folders and extensions
FILES_DICT = {'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
              'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
              'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
              'video': ['AVI', 'MP4', 'MOV', 'MKV'],
              'archives': ['ZIP', 'GZ', 'TAR']
              }

files_list = []

def ext_dict_normalize(files_dict):
    """Change all values in dict to lower case

    :param files_dict: dict
    :return: lower values in dict
    """
    for key, values in files_dict.items():
        for i in range(len(values)):
            values[i] = values[i].lower()


def file_handler(path: Path):
    """ Processing each file based on the dictionary: renaming - by the normalize function
         create folder by dictionary key if missing
         moving the file to this folder, adding it to the list of known extensions depending on the dictionary key
         for archives: create folder by dictionary key, create subfolder by archive name, unpack archive into subfolder
         listing
         for unknown - create a list of unknown extensions

    :param path: path
    :return: make manipulation with files
    """

    file_full_name = path.name
    file_ext = file_full_name.split('.')[-1].lower()
    new_folder_name = os.path.join(str(base_folder), 'Unknown')
    for key, value in FILES_DICT.items():
        # if the extension is present in the dictionary
        if file_ext in value:
            new_folder_name = os.path.join(str(base_folder), key)
    # create folder by dictionary key
    os.makedirs(new_folder_name, exist_ok=True)
    # create a new file path with a changed name
    new_file_path = os.path.join(new_folder_name, file_full_name)
    # move file to destination folder
    shutil.move(str(path), new_file_path)


def get_dir_elements(path: Path):
    """ we get access to all elements of the directory, taking into account attachments

    :param path: path
    :return: None
    """
    global files_list
    for element in path.iterdir():
        # if is file:
        if element.is_file():
            # file_handler(element)  # do file processing
            files_list.append(element)
        # if folder:
        if element.is_dir():
            if element.name in FILES_DICT or not os.listdir(str(element)):
                # do not touch empty and folders from the dictionary
                continue
            # get_dir_elements(element)
            Thread(target=get_dir_elements, args=(element,)).start()
            # with ThreadPoolExecutor(max_workers=10) as executor:
            #     executor.map(get_dir_elements, (element,))
    # return files_list


def remove_empty_folder(path: Path):
    """ remove all empty folder in path folder

    :param path: path
    :return: None
    """
    for element in path.iterdir():
        if element.is_dir():
            if not os.listdir(str(element)):
                os.rmdir(str(element))  # delete folder
                continue
            remove_empty_folder(element)


def main(base_folder):
    """ Main function: Normalize dictionary of extension to lower case
    processes items from a folder
    remove empty folder

    :param base_folder: path
    :return: print result list from result_dictionary
    """
    path = Path(base_folder)
    ext_dict_normalize(FILES_DICT)
    start_list = monotonic()
    get_dir_elements(path)
    print(f'List create is {monotonic()-start_list}')
    start_exec = monotonic()
    with ThreadPoolExecutor(max_workers=10000) as executor:
        executor.map(file_handler, files_list)
    print(f'Executor time: {monotonic()-start_exec}')
    remove_empty_folder(path)


if __name__ == '__main__':
    # base_folder = input('Enter folder for sort: ')
    base_folder = 'd:\\Test\\'
    # check if the specified folder exists and is folder
    if not (os.path.exists(base_folder) and Path(base_folder).is_dir()):
        print('Path incorrect')
        exit()
    start = monotonic()
    main(base_folder)
    print(f'Run time {monotonic()-start}')
