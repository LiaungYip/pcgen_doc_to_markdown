import os
import shutil

import bs4

from config import base_output_dir, base_in_dir
from file_list import files
from html2soup import break_into_sections
from process_section import ProcessSection
from write_markdown import print_to_markdown

shutil.rmtree(base_output_dir)

def process_file(input_file_path, output_dir, relpath):
    with open(input_file_path, mode="r") as in_file:
        whole_file_html = in_file.read()

    whole_file_soup = bs4.BeautifulSoup(whole_file_html)

    # Remove all spurious "\n" strings, which are inserted whenever the HTML had
    # whitespace between tags
    for element in whole_file_soup.find_all(text=u"\n"):
        element.extract()

    # Delete all comments, since they complicate parsing.
    # They would not survive conversion to Markdown anyway
    for comments in whole_file_soup.findAll(text=lambda text: isinstance(text, bs4.Comment)):
        comments.extract()

    body = whole_file_soup.body # HTML <body>
    soup_sections = break_into_sections(body) # Break up by <hr /> tags

    for soup_section in soup_sections:
        processed_section = ProcessSection(soup_section)
        print_to_markdown(processed_section, output_dir, relpath)


def create_folder_if_not_exist(full_dir_path):
    if os.path.exists(full_dir_path) and os.path.isdir(full_dir_path):
        return
    os.makedirs(full_dir_path)

for relpath in files:
    dir, fn = os.path.split(relpath)
    fn, ext = os.path.splitext(fn)

    input_file_name = os.path.join (base_in_dir, relpath)
    output_dir = os.path.join(base_output_dir, dir, fn)
    create_folder_if_not_exist(output_dir)

    try:
        process_file(input_file_name, output_dir, relpath)
    except Exception as e:
        print "Died while trying to process file:", relpath
        raise
