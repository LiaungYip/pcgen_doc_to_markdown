import os


def create_folder_if_not_exist(full_dir_path):
    if os.path.exists(full_dir_path) and os.path.isdir(full_dir_path):
        return
    os.makedirs(full_dir_path)