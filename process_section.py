import copy
import re

import bs4
import pypandoc
import html2text

from bs_util import condense_whitespace, destroy_element, get_parent_p


def find_anchor(soup):
    # Finds all <a> tags - including named anchors, but also <a href="...">
    # hyperlinks.
    anchors = soup.find_all(name="a")
    for a in anchors:
        # Filter named anchors from outbound hyperlinks
        if a.has_attr("id") and a.has_attr("name"):
            # Malformed HTML - should be corrected in original docs
            assert a["id"] == a["name"]
            return a["id"]
    return None


def find_status(soup):
    # Extract information about tag's status vs. PCGen release version.
    #
    # This information is usually contained in a <p> tag with one of the
    # collowing CSS classes: .lstnew, .lststatus, .lstdep (deprecated),
    # .lstupnew (updated / new), or .new .
    #
    # Returns a string, or None.
    #
    # *** Removes the <p> tag from the Soup once complete. *** Since the
    # same <p> tag usually also contains the named anchor (i.e. <a
    # id="bonus" name="bonus"> you must extract the named anchor first.
    #
    # Examples from the wild:
    #
    # "New 5.5"
    # "Updated 5.7.1"
    # "New 5.10.1+"
    # "New 6.01.03"
    # "deprecated 6.03.00 - Remove for 6.6 - Use BONUS:SAVE"

    for css_style in ("lstnew", "lststatus", "lstdep", "lstupnew", "new",):
        element = soup.find(name="p", attrs={"class": css_style})
        if element:
            break

    if element is None:
        return None

    text = " ".join(element.stripped_strings)
    text = text.replace("***", "")
    text = condense_whitespace(text)
    text = text.strip()

    destroy_element(element)  # Mutates the soup!

    return text


def find_tag_parameters(soup):
    # Typical example from docs:
    #
    # Tag Name: BONUS:WEAPONPROF=x|y,y|z
    #   - Variables Used (x): Text (Weapon proficiency name)
    #   - Variables Used (x): TYPE.Text (Weapon proficiency type)
    #   - Variables Used (y): Property (Weapon proficiency property)
    #   - Variables Used (z): Number, variable or formula (Number to add)
    params = list()

    param_soup = bs4.BeautifulSoup()
    param_soup.append(bs4.BeautifulSoup.new_tag(param_soup, 'ul'))

    variables_used_re = re.compile("\s*Variables Used.*")
    variables_used = soup.find_all(string=variables_used_re)

    for v in variables_used:
        element = get_parent_p(v)
        del element["class"]
        element.name = "li"
        if element.strong:
            element.strong.unwrap()
        param_soup.ul.append(copy.copy(element))
        # assert element.find(
        #     "a") is None, "Help! Hyperlinks in something I'm converting to Plain Text! %s" % element
        # text = element.get_text(" ", strip=True)
        # # Extract "x" from "Variables Used (x):"
        # text = re.sub("Variables Used \((\w)\)", "\g<1>", text)
        # text = condense_whitespace(text)
        # params.append(text)
        destroy_element(element)  # Mutates the soup!

    # params_markdown = "\n".join(["-   " + p for p in params])
    # params_markdown = pypandoc.convert(unicode(param_soup), "md", "html")
    params_markdown = html2text.html2text(unicode(param_soup))
    params_markdown = re.sub("Variables Used \((\w)\)", "\g<1>",
                             params_markdown)

    return params_markdown


def find_tag_syntax(soup):
    # Usually looks like this:
    # <p class="indent0"><strong>Tag Name:</strong> BONUS:CHECKS|x,x|y</p>
    tag_name_re = re.compile("Tag\s*Name:")
    element = soup.find(string=tag_name_re)
    if element is None:
        return None

    # Climb up the tree until we get to the element tag.
    #
    # Note - sometimes it's <p><strong> in which case we need to go up two levels.
    #
    # But occasionally, the doc writer forgot the <strong> and we must only go up one level.
    #
    element = get_parent_p(element)

    # text = " ".join([s.strip() for s in element.stripped_strings])
    text = element.get_text(strip=True)
    # Needs to be a regex because sometimes, it's "Tag Name", and other times, it's "Tag\nName". WTF?
    text = re.sub("\s*Tag\s*Name:", "", text)

    destroy_element(element)  # Mutates the soup!
    return text


def convert_indent1_headers(soup):
    # Headings are currently marked using something like:
    #
    # <p class="indent1"><strong>Where it is used:</strong></p>
    #
    # Turn these into H2's.
    indent1 = soup.find_all(name="p", attrs={"class": "indent1"})
    for x in indent1:
        text = x.get_text(" ", strip=True)
        if re.match("What it does|Example|Where it is used", text,
                    flags=re.IGNORECASE):
            del x["class"]
            x.name = "h2"
            x.string = text.strip(":")


def process_tag_doc_section(soup):
    # Convert a PCGen element documentation section from HTML to markdown.
    # Attempt to discover features like:
    # - Anchor name, i.e. <a id="abilitypool" name="abilitypool">
    #     -> inbound link name
    # - Tag status, i.e. "New in 5.11.1"
    anchor = find_anchor(soup)  # Must be run before find_status()
    status = find_status(soup)
    syntax = find_tag_syntax(soup)
    params = find_tag_parameters(soup)
    # params = None
    convert_indent1_headers(soup)
    # md = pypandoc.convert(unicode(soup), 'md', format="html")
    md = html2text.html2text(unicode(soup))

    return {
        "anchor": anchor,
        "status": status,
        "syntax": syntax,
        "parameters": params,
        "md": md,
        "soup": soup,
    }
