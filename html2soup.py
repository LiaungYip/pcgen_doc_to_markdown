import copy

import bs4


def break_into_sections(soup):
    sections = [bs4.BeautifulSoup(), ]
    # for n, element in enumerate(list(body.children)):
    for element in soup.children:
        if element.name != "hr":
            # Note, by default, bs4.append() deletes element from tree, before
            # appending to new tree.
            #
            # copy.copy() used to clone element independent of old tree. New
            # support in Beautiful Soup 4.4.
            #
            # See: http://stackoverflow.com/questions/23057631/clone-element-with-beautifulsoup
            sections[-1].append(copy.copy(element))
        else:  # <hr /> encountered. Start a new section
            sections.append(bs4.BeautifulSoup())
    return sections