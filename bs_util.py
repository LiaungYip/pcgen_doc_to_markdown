import re
import bs4


def condense_whitespace(text):
    return re.sub("\s+", " ", text)


def destroy_element(element):
    # Took a bit of futzing around to arrive at this solution.
    # previously was using element.replace_with("") to work around a bug
    element.decompose()


def get_parent_p(element):
    # Recursively ascend the tree until we find the enclosing <p> tag.
    p = element
    while isinstance(p, bs4.NavigableString) or p.name != "p":
        p = p.parent
    return p


def strip_whitespace(soup):
    print unicode(soup)
    for child in soup.descendants:
        print "%s ->`%s`<-" % (child.name, child.string)
        if child.string is None:
            continue
        if re.match("^\s*$", child.string):
            child.string = ""
            # print child
            # if child.name in (None, "pre", "code"):
            #     continue
            # if child.string:
            #     child.string = child.string.strip
            # print child