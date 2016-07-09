import os
from pprint import pprint

output_dir = "G:\\"

md_template = """
# {anchor}

## Status

{status}

## Syntax

`{syntax}`

## Parameters

{parameters}

{md}
"""

def generate_file_name(name):

    def assemble_name(seq = None):
        if seq is None:
            return os.path.join(output_dir, name + ".md")
        else:
            return os.path.join(output_dir, "%s_%i.md" % (name, seq))

    default_name = "front_matter"
    if name is None:
        name = default_name

    if not os.path.exists(assemble_name()):
        return assemble_name()

    # If the file already exists, try "foo_1.md", "foo_2,md", ...
    n = 1
    while os.path.exists(assemble_name(n)):
        n += 1
    return assemble_name(n)



def print_to_markdown(processed_section):
    output_file_path = generate_file_name(processed_section["anchor"])
    print ("Writing: %s" % output_file_path)

    content = md_template.format(**processed_section)

    with open(output_file_path, "wb") as out_file:
        out_file.write(content)