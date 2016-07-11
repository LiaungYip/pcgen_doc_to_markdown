from pprint import pprint

from file_list import files

files = [f.replace(".html", "") for f in files]
files = [f.replace("\\", "/") for f in files]

# prefixes = set()
# for f in files:
#     a, b = os.path.split(f)
#     prefixes.add((a,b,))
#     while a:
#         a, b = os.path.split(a)
#         prefixes.add((a,b,))

pairs = set()

for f in files:
    parts = f.split("/")
    for parent, child in zip(parts[:-1], parts[1:]):
        pairs.add((parent, child))

# pprint(pairs)

template = """[[menu.main]]
    name = "{name}"
    identifier = "{child}"
    parent = "{parent}"
"""

out_file = open("G:/menu.toml", "w")

for pair in pairs:
    parent = pair[0]
    child = pair[1]

    name = child
    for trash in ["filestagpages","datafiles","globalfiles","gamemode","systemfiles"]:
        name = name.replace(trash,"")

    out_file.write(template.format(parent = parent, child = child, name = name))

out_file.close()
