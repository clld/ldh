import pathlib

import attr
from clld.cliutil import Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from cldfcatalog import Catalog
from pyglottolog import Glottolog
from clld_glottologfamily_plugin.util import load_families
from clldutils import licenses

import ldh
from ldh import models
from ldh.util import iter_posts
from ldh import pure
from ldh import zenodo

PROJECT_DIR = pathlib.Path(__file__).parent.parent.parent.parent


def main(args):
    gl_dir = PROJECT_DIR.parent / 'glottolog' / 'glottolog'
    gl_dir = pathlib.Path(input('Path to clone of glottolog/glottolog [{}]: '.format(gl_dir)) or gl_dir)
    assert gl_dir.exists()
    with Catalog(gl_dir, tag=input('Glottolog version: ') or None) as cat:
        _main(Data(), Glottolog(gl_dir))


def _main(data, glottolog):
    languoids = list(glottolog.languoids())
    lbyi = {l.iso: l for l in languoids if l.iso}

    dataset = common.Dataset(
        id='ldh',
        name='Language Description Heritage',
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license="https://creativecommons.org/licenses/by/4.0/",
        domain='ldh.clld.org',
        contact='ldh@eva.mpg.de',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)

    DBSession.add(common.Editor(
        dataset=dataset,
        contributor=common.Contributor(id='forkel', name='Robert Forkel')))

    ls = set()
    for post in iter_posts():
         if post.pure_item_id:
            item = pure.Item.from_json(post.pure_item_id)
            src = data['Description'].get(item.id)
            if not src:
                src = data.add(
                    models.Description, item.id,
                    id=item.id,
                    description=item.title,
                    name=item.name,
                    bibtex_type=EntryType.get(item.bibtex_type),
                    year=item.year,
                    title=item.title,
                    address=item.publisher.get('place') if item.publisher else None,
                    publisher=item.publisher.get('publisher') if item.publisher else None,
                    author=' and '.join(item.authors),
                    editor=' and '.join(item.editors),
                    pid=item.doi or item.pid,
                    pid_type='doi' if item.doi else 'hdl',
                )
                DBSession.flush()
                for file in item.files:
                    if file.visibility == 'PUBLIC' \
                            and file.metadata["contentCategory"] == "any-fulltext"\
                            and file.storage == 'INTERNAL_MANAGED':
                        assert file.mimeType == 'application/pdf'
                        DBSession.add(common.Source_files(
                            id=file.pid.replace('/', '__'),
                            name=file.name,
                            object_pk=src.pk,
                            mime_type=file.mimeType,
                            jsondata=dict(
                                size=file.size,
                                license=attr.asdict(file.license) if file.license else None),
                        ))
            for iso in item.isocodes:
                if iso in lbyi:
                    gl = lbyi[iso]
                    l = data['LDHLanguage'].get(iso)
                    if not l:
                        l = data.add(models.LDHLanguage, iso, id=iso, name=gl.name)
                    DBSession.flush()
                    if (item.id, iso) not in ls:
                        DBSession.add(common.LanguageSource(language_pk=l.pk, source_pk=src.pk))
                        ls.add((item.id, iso))

    for item in zenodo.iter_items():
        src = data.add(
            models.Description, item.id,
            id=item.id,
            description=item['metadata']['title'],
            name=item.name,
            bibtex_type=EntryType.get('misc' if  item.bibtex_type == 'other' else item.bibtex_type),
            year=item.year,
            title=item['metadata']['title'],
            publisher='Zenodo',
            author=' and '.join(a['name'] for a in item['metadata']['creators']),
            pid=item['metadata']['doi'],
            pid_type='doi',
        )
        DBSession.flush()
        for file in item['files']:
            license = licenses.find(item['metadata']['license']['id'])
            DBSession.add(common.Source_files(
                id=file['checksum'].replace('md5:', ''),
                name=file['key'],
                object_pk=src.pk,
                mime_type='application/' + file['type'],
                jsondata=dict(
                    size=file['size'],
                    url=file['links']['self'],
                    license=attr.asdict(license) if license else None),
            ))

        for kw in item['metadata'].get('keywords', []):
            if not kw.startswith('iso:'):
                continue
            iso = kw.replace('iso:', '')
            if iso in lbyi:
                gl = lbyi[iso]
                l = data['LDHLanguage'].get(iso)
                if not l:
                    l = data.add(models.LDHLanguage, iso, id=iso, name=gl.name)
                DBSession.flush()
                if (item.id, iso) not in ls:
                    DBSession.add(common.LanguageSource(language_pk=l.pk, source_pk=src.pk))
                    ls.add((item.id, iso))


    load_families(
        data,
        data['LDHLanguage'].values(),
        glottolog_repos=glottolog.repos,
        isolates_icon='tcccccc')
