# C:\Users\lws\gits\pcgen\docs\listfilepages\globalfilestagpages\globalfilesbonus.html

import bs4
import os

from html2soup import break_into_sections
from process_section import ProcessSection
from write_markdown import print_to_markdown
from file_list import files


def process_file(input_file_path, output_dir):
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
        print_to_markdown(processed_section, output_dir)


base_output_dir = r"G:\\"
base_in_dir = r"C:\Users\lws\gits\pcgen\docs\\"

def create_folder_if_not_exist(full_dir_path):
    if os.path.exists(full_dir_path) and os.path.isdir(full_dir_path):
        return
    os.makedirs(full_dir_path)

for path in files:
    dir, fn = os.path.split(path)
    fn, ext = os.path.splitext(fn)


    # ex1 = base_in_dir + r"\listfilepages\globalfilestagpages\globalfilesbonus.html"
    input_file_name = base_in_dir + path
    output_dir = os.path.join(base_output_dir, dir, fn)
    create_folder_if_not_exist(output_dir)
    try:
        process_file(input_file_name, output_dir)
    except Exception as e:
        print "Died while trying to process file:", path
        raise
