import json
import collections
import re

import attr
from clldutils.source import Source
from clldutils.licenses import find

from ldh.util import REPOS


@attr.s
class Rights(object):
    name = attr.ib()
    url = attr.ib()


@attr.s
class Creator(object):
    type = attr.ib(default='PERSON')
    role = attr.ib(default='AUTHOR')
    name = attr.ib(default=None)
    givenName = attr.ib(default=None)
    familyName = attr.ib(default=None)
    completeName = attr.ib(default=None)
    alternativeNames = attr.ib(default=attr.Factory(list))
    organizations = attr.ib(default=attr.Factory(list))
    identifier = attr.ib(default=None)
    identifierPath = attr.ib(default=None)

    @classmethod
    def from_value(cls, v):
        d = {k: v_ for k, v_ in v.items() if k not in ['person', 'organization']}
        for k in ['person', 'organization']:
            if k in v:
                d.update(v[k])
        return cls(**d)

    @property
    def lastname(self):
        if self.familyName:
            return self.familyName
        return self.fullname

    @property
    def fullname(self):
        if self.type == 'ORGANIZATION':
            return self.name
        if self.completeName:
            return self.completeName
        return '{0.familyName}, {0.givenName}'.format(self)

    @property
    def affiliation(self):
        for org in self.organizations:
            if org['name'] != 'External Organizations':
                return org['name']


@attr.s
class Date(object):
    date = attr.ib()
    type = attr.ib()

    @classmethod
    def from_kv(cls, k, v):
        return cls(v, k.replace('date', ''))


def grouped(iterable, key, value):
    res = collections.defaultdict(list)
    for item in (iterable or []):
        res[item.get(key)].append(item.get(value))
    return res


@attr.s
class File(object):
    objectId = attr.ib()
    name = attr.ib()
    creationDate = attr.ib()
    visibility = attr.ib()
    pid = attr.ib()
    content = attr.ib()
    storage = attr.ib()
    mimeType = attr.ib()
    size = attr.ib()
    metadata = attr.ib()

    @property
    def license(self):
        return find((self.metadata.get('license') or '').strip())

    @classmethod
    def from_value(cls, d):
        fields = [f.name for f in attr.fields(cls)]
        return cls(**{f: d.get(f) for f in fields})


def valid_isocodes(instance, attribute, value):
    if not all(bool(re.match('[a-z]{3}$', s)) for s in value):
        raise ValueError()


@attr.s
class Item(object):
    id = attr.ib()
    pid = attr.ib(converter=lambda s: s.replace('hdl:', ''))
    doi = attr.ib()
    title = attr.ib()
    genre = attr.ib()
    isocodes = attr.ib(validator=attr.validators.optional(valid_isocodes))
    creators = attr.ib(converter=lambda i: [Creator.from_value(a) for a in i])
    publisher = attr.ib()
    dates = attr.ib(converter=lambda i: [Date.from_kv(*a) for a in i])
    degree = attr.ib()
    files = attr.ib(converter=lambda i: [File.from_value(a) for a in i])

    @classmethod
    def from_json(cls, id_):
        with REPOS.joinpath('json', 'pure', id_ + '.json').open() as fp:
            data = json.load(fp)

        identifiers = grouped(data['metadata'].get('identifiers'), 'type', 'id')
        subjects = grouped(data['metadata'].get('subjects'), 'type', 'value')
        return cls(
            id=id_,
            pid=data['objectPid'],
            doi=identifiers.get('DOI', [None])[0],
            title=data['metadata']['title'].strip(),
            isocodes=[s.split('-')[0].strip() for s in subjects.get('ISO639_3', []) if s],
            creators=data['metadata']['creators'],
            publisher=data['metadata'].get('publishingInfo'),
            dates=[(k, v) for k, v in data['metadata'].items() if k.startswith('date')],
            genre=data['metadata']['genre'],
            degree=data['metadata'].get('degree'),
            files=data['files'],
        )

    @property
    def year(self):
        for date in self.dates:
            if date.type and 'Published' in date.type:
                return date.date.split('-')[0]
        for date in self.dates:
            if date.type and 'Accepted' in date.type:
                return date.date.split('-')[0]

    @property
    def name(self):
        creators = [c for c in self.creators if c.role == 'AUTHOR'] or \
                   [c for c in self.creators if c.role == 'EDITOR']
        if len(creators) < 3:
            res = ' and '.join([c.lastname for c in creators])
        else:
            res = creators[0].lastname + ' et al.'
        if self.year:
            res += ' {0}'.format(self.year)
        return res

    @property
    def authors(self):
        return [c.fullname for c in self.creators if c.role == 'AUTHOR']

    @property
    def editors(self):
        return [c.fullname for c in self.creators if c.role == 'EDITOR']

    @property
    def bibtex_type(self):
        for bibtex, genres in {
            'book': ['BOOK', 'MONOGRAPH', 'COLLECTED_EDITION'],
            'inbook': ['BOOK_ITEM'],
            'phdthesis': ['THESIS'],
            'article': ['ARTICLE', 'PAPER'],
            'proceedings': ['PROCEEDINGS'],
            'inproceedings': ['CONFERENCE_PAPER'],
            'incollection': ['CONTRIBUTION_TO_COLLECTED_EDITION'],
        }.items():
            if self.genre in genres:
                res = bibtex
                if res == 'phdthesis' and self.degree == 'MASTER':
                    res = 'mastersthesis'
                return res

    def as_source(self):
        kw = {
            'title': self.title,
        }
        if self.authors:
            kw['author'] = ' and '.join(self.authors)
        if self.editors:
            kw['editor'] = ' and '.join(self.editors)
        return Source(self.bibtex_type, self.id, **kw)