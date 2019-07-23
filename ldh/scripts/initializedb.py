import sys
import pathlib

import attr
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import EntryType
from pyglottolog import Glottolog
from clld_glottologfamily_plugin.util import load_families

import ldh
from ldh import models
from ldh.util import iter_posts
from ldh import pure


def main(args):
    data = Data()
    glottolog = Glottolog(pathlib.Path(ldh.__file__).parent.parent.parent.parent.joinpath('glottolog', 'glottolog'))
    languoids = list(glottolog.languoids())
    lbyi = {l.iso: l for l in languoids if l.iso}

    dataset = common.Dataset(
        id='ldh',
        name='Language Description Heritage',
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://www.shh.mpg.de",
        license="https://creativecommons.org/licenses/by/4.0/",
        domain='ldh.clld.org',
        contact='ldh@shh.mpg.de',
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

    load_families(
        data,
        data['LDHLanguage'].values(),
        glottolog_repos=glottolog.repos,
        isolates_icon='tcccccc')


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """


if __name__ == '__main__':  # pragma: no cover
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
