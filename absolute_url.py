# Convert all URLs in the documentation into absolute urls.

import bs4

from file_list import all_files
from url_transform import absolute_href

import os.path

root = "C:/Users/lws/gits/pcgen/docs/"

n_files = 0
n_blank_href = 0
n_no_change = 0
n_changed = 0

for f in all_files:
    f = os.path.join(root,f)
    with open(f, mode="r") as in_file:
        whole_file_html = in_file.read()
    whole_file_soup = bs4.BeautifulSoup(whole_file_html)

    anchors = whole_file_soup.find_all("a")

    for a in anchors:
        if not a.has_attr("href"):
            continue
        h1 = a["href"]


        if h1.strip() == "":
            print 'DELETING blank href="" attribute\n'
            del a["href"]
            n_blank_href += 1
            continue

        h2 = absolute_href(h1, f, root)
        h2 = h2.replace("\\","/")

        if h1 == h2:
            print 'NO CHANGE: %s already absolute' % h2
            n_no_change += 1
            continue

        else:
            print "CHANGING: In file %s:\nCHANGING: from %s\nCHANGING: to   %s\n" % (f, h1, h2)
            a["href"] = h2
            n_changed += 1

    with open(f, mode="wb") as out_file:
        out_file.write(unicode(whole_file_soup).encode("utf-8"))

    n_files += 1

print """
BLANK HREF : %4i
NO CHANGE  : %4i
CHANGED    : %4i
NUM FILES  : %4i
""" % (n_blank_href, n_no_change, n_changed, n_files)