import datetime
import os

md_template = u"""+++
date = "{date}"
title = "{anchor}"
original_url = "{original_url}"

[menu.main]
    identifier = "{id}"
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
    def seq_name(seq=None):
        if seq is None:
            return anchor_name
        else:
            return "%s_%i" % (anchor_name, seq)

    def full_path(seq = None):
        return os.path.join(output_dir, seq_name(seq) + ".md")

    default_name = "index"
    if anchor_name is None:
        anchor_name = default_name

    if not os.path.exists(full_path()):
        return seq_name()

    # If the file already exists, try "foo_1.md", "foo_2,md", ...
    n = 1
    while os.path.exists(full_path(n)):
        n += 1
    return seq_name(n)


def print_to_markdown(processed_section, output_dir, relpath):
    # Sample relpath:
    # "listfilepages\globalfilestagpages\globalfilesbonus.html"

    anchor = processed_section["anchor"]
    output_file_name = generate_file_name(output_dir, anchor)
    output_file_path = os.path.join(output_dir, output_file_name + ".md")
    if processed_section["anchor"] is None and processed_section["md"].strip() == "":
        assert "index" in output_file_path
        print ("Skipping: %s (blank)" % output_file_path)
        return
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

    id = parent + "_" + output_file_name
    # if anchor:
    #     id = id + "_" + anchor

    content = md_template.format(original_url=original_url, date=date,
                                 parent=parent, id = id, **processed_section)

    with open(output_file_path, "wb") as out_file:
        out_file.write(content.encode('utf-8'))
