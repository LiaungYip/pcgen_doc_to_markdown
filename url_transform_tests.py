import unittest
from url_transform import absolute_href

class TestUrlTransform (unittest.TestCase):
    def test_external_urls(self):
        test_urls = [
            "http://www.google.com",
            "https://www.google.com",
            "ftp://www.google.com",
            "mailto:liaung@gmail.com",
        ]
        for test_url in test_urls:
            out = absolute_href(test_url,"C:/","C:/")
            expected = test_url
            self.assertEqual(out, expected)

    def test_bare_anchor(self):
        out = absolute_href("#foo","C:/root/a.html","C:/root/")
        expected = "/a.html#foo"
        self.assertEqual(out, expected)

    def test_same_folder(self):
        out = absolute_href("b.html", "C:/root/a.html", "C:/root/")
        expected = "/b.html"
        self.assertEqual(out, expected)

        out = absolute_href("b.html#anch", "C:/root/a.html", "C:/root/")
        expected = "/b.html#anch"
        self.assertEqual(out, expected)

    def test_down_folders(self):
        out = absolute_href("f2/b.html", "C:/root/a.html", "C:/root/")
        expected = "/f2/b.html"
        self.assertEqual(out, expected)

        out = absolute_href("f2/b.html", "C:/root/f1/a.html", "C:/root/")
        expected = "/f1/f2/b.html"
        self.assertEqual(out, expected)

    def test_up_folders(self):
        out = absolute_href("../../f3/b.html", "C:/root/f1/f2/a.html", "C:/root/")
        expected = "/f3/b.html"
        self.assertEqual(out, expected)

        out = absolute_href("../../f3/b.html#anch", "C:/root/f1/f2/a.html", "C:/root/")
        expected = "/f3/b.html#anch"
        self.assertEqual(out, expected)