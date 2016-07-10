import datetime
import os

md_template = u"""+++
date = "{date}"
title = "{anchor}"
original_url = "{original_url}"

[menu.main]
    parent = "{parent}"
+++
# {anchor}

## Status

{status}

## Syntax

`{syntax}`

## Parameters

{parameters}

{md}
"""


def generate_file_name(output_dir, anchor_name):
    def assemble_name(seq=None):
        if seq is None:
            return os.path.join(output_dir, anchor_name + ".md")
        else:
            return os.path.join(output_dir, "%s_%i.md" % (anchor_name, seq))

    default_name = "front_matter"
    if anchor_name is None:
        anchor_name = default_name

    if not os.path.exists(assemble_name()):
        return assemble_name()

    # If the file already exists, try "foo_1.md", "foo_2,md", ...
    n = 1
    while os.path.exists(assemble_name(n)):
        n += 1
    return assemble_name(n)


def print_to_markdown(processed_section, output_dir, relpath):
    # Sample relpath:
    # "listfilepages\globalfilestagpages\globalfilesbonus.html"

    anchor = processed_section["anchor"]
    output_file_path = generate_file_name(output_dir, anchor)
    print ("Writing: %s" % output_file_path)

    date = str(datetime.date.today())

    # Insert the original URL as a metadata field - so we can mass-rewrite
    # hyperlinks later
    original_url = relpath
    if anchor:
        original_url = original_url + "#" + anchor
    # On windows, path separator is "\" which is no good.
    original_url = original_url.replace("\\","/")

    # Determine what the parent menu item should be
    dir, file = os.path.split(relpath)
    parent = file.replace(".html", "")

    content = md_template.format(original_url=original_url, date=date,
                                 parent=parent, **processed_section)

    with open(output_file_path, "wb") as out_file:
        out_file.write(content.encode('utf-8'))
