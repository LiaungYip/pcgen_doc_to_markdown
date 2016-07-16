import os.path

def absolute_href(in_href, in_source_file_path, root_path):
    # Make sure the in_source_file_path is an absolute path
    assert (os.path.abspath(in_source_file_path) == os.path.normpath(in_source_file_path))

    # Link is already absolute
    if in_href.startswith("/"):
        return in_href

    # Don't touch external links
    # i.e. http:, https:, ftp:, mailto:
    if ":" in in_href:
        return in_href

    # Anchor is in same document
    if in_href.startswith("#"):
        rel_path = os.path.relpath(in_source_file_path, root_path)
        return "/" + rel_path + in_href

    # Example:
    # in_source_file_path = C:/root/f1/a.html,
    # which contains a link <a href="../f2/b.html#anch">.
    # so in_href = "../f2/b.html#anch".
    #
    # Desired root is "C:/root".

    # in_source_file_dir = "C:/root/f1"
    in_source_file_dir, _ = os.path.split(in_source_file_path)

    # href_path = "../f2/b.html", href_anchor = "anch"
    if "#" in in_href:
        href_path, href_anchor = in_href.split("#")
        anchor = "#" + href_anchor
    else:
        href_path = in_href
        anchor = ""

    # href_dir = "../f2", href_file = "b.html"
    href_dir, href_file = os.path.split(href_path)

    # abs_dir = "C:/root/f1/../f2"
    abs_dir = os.path.join (in_source_file_dir, href_dir)
    # abs_dir = "C:/root/f2"
    abs_dir = os.path.normpath(abs_dir)

    # abs_path = "C:/root/f2/b.html"
    abs_path = os.path.join(abs_dir, href_file)
    # abs_path = "C:/root/f2/b.html#anch"
    abs_path = abs_path + anchor

    # rel_path = "/f2/b.html#anch"
    rel_path = "/" + os.path.relpath(abs_path, root_path)

    # Filesystem urls on Windows use "\" as path separator
    # Web URLs must always use "/"
    out_href = rel_path.replace("\\","/")

    return out_href
#
# print absolute_href("../f2/b.html#anch","C:/root/f1/a.html", "C:/root")