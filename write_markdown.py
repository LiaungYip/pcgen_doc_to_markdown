import os
from pprint import pprint

output_dir = "G:\\"
default_name = "front_matter_"
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


def print_to_markdown(processed_section):
    pprint(processed_section)
    if processed_section["anchor"] is None:
        fn = default_name + ".md"
    else:
        fn = processed_section["anchor"] + ".md"

    content = md_template.format(**processed_section)
    out_file = open(os.path.join(output_dir, fn), "wb")
    out_file.write(content)
    out_file.close()