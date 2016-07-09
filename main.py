# C:\Users\lws\gits\pcgen\docs\listfilepages\globalfilestagpages\globalfilesbonus.html

import bs4

from html2soup import break_into_sections
from process_section import ProcessSection
from write_markdown import print_to_markdown


def process_file(input_file_path):
    with open(input_file_path, mode="r") as in_file:
        whole_file_html = in_file.read()

    whole_file_soup = bs4.BeautifulSoup(whole_file_html)

    # Remove all spurious "\n" strings, which are inserted whenever the HTML had
    # whitespace between tags
    for element in whole_file_soup.find_all(text=u"\n"):
        element.extract()

    body = whole_file_soup.body # HTML <body>
    soup_sections = break_into_sections(body) # Break up by <hr /> tags

    for soup_section in soup_sections:
        processed_section = ProcessSection(soup_section)
        print_to_markdown(processed_section)


ex1 = "C:\Users\lws\gits\pcgen\docs\listfilepages\globalfilestagpages\globalfilesbonus.html"
process_file(ex1)
