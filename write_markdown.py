import datetime
import os

tag_doc_markdown_template = u"""+++
date = "{date}"
title = "{title}"
original_url = "{original_url}"

[menu.main]
    identifier = "{id}"
    name = "{menuname}"
    parent = "{parent}"
+++

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


def print_tag_doc_to_markdown(processed_section, output_dir, relpath):
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

    if anchor:
        menuname = anchor.upper()
        title = menuname
    else:
        menuname = parent.upper()
        title = menuname

    content = tag_doc_markdown_template.format(title = title, original_url=original_url, date=date,
                                               parent=parent, id = id, menuname = menuname, **processed_section)

    with open(output_file_path, "wb") as out_file:
        out_file.write(content.encode('utf-8'))


def print_normal_page_to_markdown(soup, output_dir, relpath):
    # Sample relpath:
    # "listfilepages\globalfilestagpages\globalfilesbonus.html"
    dir, file = os.path.split(relpath)
    file, _ = os.path.splitext(file)
    output_file_path = os.path.join(output_dir, dir) + "/" + file + ".md"

    print ("Writing: %s" % output_file_path)

    date = str(datetime.date.today())
    original_url = relpath.replace("\\","/")

    # If there's a directory named for it, the file is an index
    # Otherwise, it's just a normal page



