#!/usr/bin/env python3
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

BASE = sys.argv[1].rstrip("/")
PAGES = ["/", "/about/", "/contact/", "/privacy/", "/blog/", "/blog/archive/"]


def get(path, accept=None):
    request = urllib.request.Request(BASE + path, headers={"Accept": accept} if accept else {})
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as error:
        response = error
    return response.status, response.headers, response.read().decode()


def assert_vary(headers):
    values = {value.strip().lower() for value in headers.get("Vary", "").split(",")}
    assert {"accept", "accept-encoding"} <= values, headers.get("Vary")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_main = False
        self.in_json_ld = False
        self.text = []
        self.json_ld = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "main":
            self.in_main = True
        if tag == "script" and attributes.get("type") == "application/ld+json":
            self.in_json_ld = True

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        if tag == "script":
            self.in_json_ld = False

    def handle_data(self, data):
        if self.in_main:
            self.text.append(data)
        if self.in_json_ld:
            self.json_ld.append(data)


for path in PAGES:
    status, headers, html = get(path, "text/html")
    assert status == 200, (path, status)
    assert headers.get_content_type() == "text/html", (path, headers.get("Content-Type"))
    assert_vary(headers)

    status, headers, markdown = get(path, "text/markdown")
    assert status == 200, (path, status)
    assert headers.get_content_type() == "text/markdown", (path, headers.get("Content-Type"))
    assert_vary(headers)
    assert markdown.lstrip().startswith("# ") and "<html" not in markdown.lower(), path

for path in ["/about/", "/contact/", "/privacy/"]:
    _, _, html = get(path, "text/html")
    parser = PageParser()
    parser.feed(html)
    assert len(" ".join(parser.text).strip()) >= 500, path

_, _, homepage = get("/", "text/html")
assert "<title>NonnoAlex | Alessandro Lo Manto</title>" in homepage
parser = PageParser()
parser.feed(homepage)
schema = json.loads("".join(parser.json_ld))
person = next(item for item in schema["@graph"] if item["@type"] == "Person")
assert person["name"] == "Alessandro Lo Manto"
assert person["alternateName"] == "NonnoAlex"
assert person["url"] == "https://nonnoalex.dev/"
assert len(person["sameAs"]) == 3

status, headers, llms = get("/llms.txt")
assert status == 200 and headers.get_content_type() == "text/plain"
assert llms.startswith("# NonnoAlex\n>")
assert "## When to use this site" in llms and "Accept: text/markdown" in llms

status, headers, sitemap = get("/sitemap.xml")
assert status == 200 and headers.get_content_type() in {"application/xml", "text/xml"}
urls = [node.text for node in ET.fromstring(sitemap).iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
for required in ["https://nonnoalex.dev/", "https://nonnoalex.dev/about/", "https://nonnoalex.dev/contact/", "https://nonnoalex.dev/privacy/"]:
    assert required in urls

for url in urls:
    path = urlparse(url).path
    for accept, content_type in [("text/html", "text/html"), ("text/markdown", "text/markdown")]:
        status, headers, body = get(path, accept)
        assert status == 200, (path, status)
        assert headers.get_content_type() == content_type, (path, headers.get("Content-Type"))
        assert_vary(headers)
        assert body.strip(), path

status, headers, robots = get("/robots.txt")
assert status == 200 and headers.get_content_type() == "text/plain"
assert "Sitemap: https://nonnoalex.dev/sitemap.xml" in robots

status, headers, atom = get("/atom.xml")
assert status == 200 and headers.get_content_type() in {"application/atom+xml", "application/xml", "text/xml"}
ET.fromstring(atom)

for accept, content_type in [("text/html", "text/html"), ("text/markdown", "text/markdown")]:
    status, headers, body = get("/__agent-readiness-missing__", accept)
    assert status == 404
    assert headers.get_content_type() == content_type
    assert "/sitemap.xml" in body and "/llms.txt" in body

print("All agent-readiness checks passed")
