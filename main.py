# C:\Users\lws\gits\pcgen\docs\listfilepages\globalfilestagpages\globalfilesbonus.html

import bs4

from html2soup import break_into_sections
from process_section import ProcessSection
from write_markdown import print_to_markdown

f = open(
    "C:\Users\lws\gits\pcgen\docs\listfilepages\globalfilestagpages\globalfilesbonus.html",
    mode="r")
contents = f.read()

bigsoup = bs4.BeautifulSoup(contents)

# Remove all spurious "\n" strings, which are inserted whenever the HTML had
# whitespace between tags
for e in bigsoup.find_all(text=u"\n"):
    e.extract()

body = bigsoup.body

sections = break_into_sections(body)

for s in sections:
    print_to_markdown(ProcessSection(s))
