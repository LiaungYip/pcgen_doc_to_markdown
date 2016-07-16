import copy

import bs4

def break_into_sections(soup):
    sections = [list(), ]
    for element in soup.children:
        if element.name != "hr":
            sections[-1].append(unicode(element))
        else:  # <hr /> encountered. Start a new section
            sections.append(list())
    return [bs4.BeautifulSoup("".join(section)) for section in sections]