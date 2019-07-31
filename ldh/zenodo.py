import json
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup as bs
from clldutils.jsonlib import load
from nameparser import HumanName

from ldh.util import REPOS


OAI = "https://zenodo.org/oai2d"
#?verb=ListRecords"
#&set=user-ldh&metadataPrefix=oai_dc"

OAI_NS = "http://www.openarchives.org/OAI/2.0/"


def get(id_, outdir, overwrite=False):
    p = outdir.joinpath('zenodo_{0}'.format(id_))
    if (not p.exists()) or overwrite:
        html = bs(requests.get(
            'https://zenodo.org/record/{0}/export/json'.format(id_)).text, 'html.parser')
        rec = json.loads(html.find('pre').text)
        outdir.joinpath('zenodo_{0}'.format(id_)).write_text(json.dumps(rec, indent=4), encoding='utf8')


class OAIResponse(object):
    def __init__(self, **params):
        params.setdefault('verb', 'ListRecords')
        res = requests.get(OAI, params=params)
        self.xml = ET.fromstring(res.text)

    def element(self, lname, parent=None, method='find'):
        return getattr(parent or self.xml, method)('.//{%s}%s' % (OAI_NS, lname))

    @property
    def resumption_token(self):
        return getattr(self.element('resumptionToken'), 'text', None)

    def iter_identifiers(self):
        for rec in self.element('record', method='findall'):
            yield self.element('identifier', parent=rec).text


def iter_identifiers(community):
    res = OAIResponse(set='user-{0}'.format(community), metadataPrefix='oai_dc')
    for rec in res.element('record', method='findall'):
        yield res.element('identifier', parent=rec).text
    while res.resumption_token:
        res = OAIResponse(resumptionToken=res.resumption_token)
        for rec in res.element('record', method='findall'):
            yield res.element('identifier', parent=rec).text


def crawl():
    outdir = REPOS / 'json' / 'zenodo'
    if not outdir.exists():
        outdir.mkdir()
    for id_ in iter_identifiers('ldh'):
        get(id_.split(':')[-1], outdir)


class Item(dict):
    def __init__(self, p):
        dict.__init__(self, load(p))
        self.id = p.stem

    @property
    def name(self):
        author_names = [HumanName(c['name']) for c in self['metadata']['creators']]
        if len(author_names) < 3:
            res = ' and '.join(a.last for a in author_names)
        else:
            res = '{0} et al.'.format(author_names[0].last)
        return '{0} {1}'.format(res, self.year)

    @property
    def year(self):
        return self['metadata']['publication_date'].split('-')[0]

    @property
    def bibtex_type(self):
        try:
            return self['metadata']['resource_type']['subtype']
        except KeyError:
            return 'misc'


def iter_items():
    for p in REPOS.joinpath('json', 'zenodo').glob('*'):
        yield Item(p)
