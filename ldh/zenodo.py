import json
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup as bs

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
