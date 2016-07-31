from pprint import pprint

from file_list import all_files, files_no_tags, files_tags

files_tags = [f.replace(".html", "") for f in files_tags]
files_tags = [f.replace("\\", "/") for f in files_tags]

pairs = set()
root_items = set()

for f in files_tags:
    parts = f.split("/")
    for parent, child in zip(parts[:-1], parts[1:]):
        pairs.add((parent, child))

files_no_tags = [f.replace(".html", "") for f in files_no_tags]
files_no_tags = [f.replace("\\", "/") for f in files_no_tags]

for f in files_no_tags:
    print f
    parts = f.split("/")
    # Trim off last thing
    parts = parts[:-1]

    if len(parts) == 1:
        root_items.add(parts[0])
    else:
        for parent, child in zip(parts[:-1], parts[1:]):
            print parent, child
            pairs.add((parent, child))

# pprint(pairs)

leaf_template = """[[menu.main]]
    name = "{name}"
    identifier = "{child}"
    parent = "{parent}"
"""

root_template = """[[menu.main]]
    name = "{name}"
    identifier = "{name}"
"""

out_file = open("G:/menu.toml", "w")

for root in root_items:
    out_file.write(root_template.format(name = root))


for pair in pairs:
    parent = pair[0]
    child = pair[1]

    name = child
    for trash in ["filestagpages","datafiles","globalfiles","gamemode","systemfiles"]:
        name = name.replace(trash,"")

    if "tagpages" in parent:
        continue

    out_file.write(leaf_template.format(parent = parent, child = child, name = name))

out_file.close()

print root_items