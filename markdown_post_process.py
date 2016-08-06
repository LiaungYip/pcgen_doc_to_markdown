import os
import io
import re
from pprint import pprint

start = "G:/pcgen-docs/content/"
file_list = []

for root, subdirs, files in os.walk(start):
    file_list.extend([os.path.join(root,f) for f in files if f.endswith(".md")])

pprint (file_list)

replacement_urls = []

# First pass
# Discover all the URLS we need to change
for f in file_list:
    with io.open(f, mode="r", encoding="utf-8") as in_file:
        md = in_file.read()

    original_url_match = re.search('original_url = "(.+?)"', md)

    original_url = original_url_match.group(1)

    if not original_url.startswith("/"):
        original_url = "/" + original_url

    rel_url = os.path.relpath(f, start)
    rel_url = rel_url.replace("\\","/")
    rel_url = "/" + rel_url
    rel_url = rel_url.replace(".md",".html")

    if original_url == rel_url:
        continue

    print "original :", original_url
    print "new      :", rel_url

    replacement_urls.append( (original_url, rel_url, ) )

pprint (replacement_urls)

# Second pass
# Actually replace all the URLS

for f in file_list:
    print "entering %s" % f
    with io.open(f, mode="r", encoding="utf-8") as in_file:
        md = in_file.read()

    for old, new in replacement_urls:
        old = "(" + old + ")"
        new = "(" + new + ")"
        md = md.replace(old,new)

    with io.open(f, mode="w", encoding="utf-8") as out_file:
        out_file.write(md)