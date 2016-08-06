# Quick and dirty stand-alone utility to find all named anchors in a give HTML file.

import bs4

infile = "C:\Users\lws\gits\pcgen\docs\list\data\install.html"
in_file_h = open(infile,"r")
soup = bs4.BeautifulSoup(in_file_h)
for a in soup.find_all("a"):
    if a.has_attr("id"):
        aid = a["id"]
        print '<li><a href="#{0}">{1}</a></li>'.format(aid, aid.upper())

