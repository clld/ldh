"""
This module will be available in templates as ``u``.

This module is also used to lookup custom template context providers, i.e. functions
following a special naming convention which are called to update the template context
before rendering resource's detail or index views.
"""
import pathlib
import hashlib
import json

import attr
from bs4 import BeautifulSoup
import requests
from clld.web.util.helpers import external_link, icon
from clld.web.util.htmllib import HTML
from clldutils.misc import format_size

REPOS = pathlib.Path(__file__).parent.parent


def file_link(file):
    content = [
        HTML.a(
            icon('file'),
            'PDF ({0})'.format(format_size(file.jsondata['size'])),
            href='http://hdl.handle.net/' + file.id.replace('__', '/'),
        )]
    license = file.jsondata['license']
    if license:
        content.append(' licensed under ')
        content.append(external_link(
            license['url'], label=license['id'].upper(), title=license['name']))
    return HTML.span(*content)


@attr.s
class Post(object):
    id = attr.ib()
    url = attr.ib()
    pure_url = attr.ib()
    html = attr.ib()
    zenodo = attr.ib(default=False)

    @property
    def pure_item_id(self):
        if self.pure_url:
            return 'item_{0}'.format(self.pure_url.split('escidoc:')[1])


def iter_posts():
    with REPOS.joinpath('posts.json').open() as fp:
        posts = json.load(fp)

    for url, (pid, md) in posts.items():
        md = md or {}
        yield Post(pid, url, md.get('url'), md.get('html'))


def get(url):
    cache = REPOS / 'build'
    if not cache.exists():
        cache.mkdir()
    fname = cache.joinpath(hashlib.md5(url.encode('utf8')).hexdigest())
    if not fname.exists():
        fname.write_text(requests.get(url).text, encoding='utf8')
    return fname.read_text(encoding='utf8')


def bs(html):
    return BeautifulSoup(html, 'lxml')
