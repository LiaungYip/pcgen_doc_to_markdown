import os
import shutil

import bs4

import bs_util
from config import base_output_dir, base_in_dir
from file_list import all_files
from filesystem_util import create_folder_if_not_exist
from html2soup import break_into_sections
from process_section import process_tag_doc_section
from write_markdown import print_tag_doc_to_markdown, print_normal_page_to_markdown

if os.path.exists(base_output_dir):
    shutil.rmtree(base_output_dir)


def process_file(input_file_path, output_dir, relpath):
    with open(input_file_path, mode="r") as in_file:
        whole_file_html = in_file.read()

    whole_file_soup = bs4.BeautifulSoup(whole_file_html)

    bs_util.delete_empty_newline_elements(whole_file_soup)
    bs_util.delete_all_comments(whole_file_soup)

    body = whole_file_soup.body  # HTML <body>

    tags_part = whole_file_soup.find(id="tag_docs")
    if tags_part:
        tag_docs_soup = tags_part.extract() # Cut the special part out of the soup
        soup_sections = break_into_sections(tag_docs_soup)  # Break up by <hr /> tags
        for soup_section in soup_sections:
            processed_section = process_tag_doc_section(soup_section)
            print_tag_doc_to_markdown(processed_section, output_dir, relpath)

    print_normal_page_to_markdown(whole_file_soup, relpath)


for relpath in all_files:
    dir, fn = os.path.split(relpath)
    fn, ext = os.path.splitext(fn)

    input_file_name = os.path.join(base_in_dir, relpath)
    output_dir = os.path.join(base_output_dir, dir, fn)

    try:
        process_file(input_file_name, output_dir, relpath)
    except Exception as e:
        print "Died while trying to process file:", relpath
        raise
