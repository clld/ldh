from pyramid.config import Configurator
from clld.interfaces import IMapMarker
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

# we must make sure custom models are known at database initialization!
from ldh import models


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # http://ldh.clld.org/category/iso639_3/aap-para-arara/
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_glottologfamily_plugin')
    config.registry.registerUtility(LanguageByFamilyMapMarker(), IMapMarker)

    # /feed/ -> /sources.atom
    """
/about/ -> /
/about/objective/ -> /about
/archive/ -> /sources
/category/allgemein/
/category/iso639_3/
/comments/feed/
/contact/ -> /contact
/feed/ -> /sources.atom
/for-authors/
/for-authors/aftersubmission/
/for-authors/contribute-your-work-to-the-ldh-collection/
/for-authors/permission-form/
/for-authors/submitting-content-to-ldh-which-has-already-been-submitted-or-published-by-another-publisher/
/for-authors/take-care-when-signing-future-contracts-with-publishers/
/for-authors/take-down-policy/
/for-authors/what-can-i-do-if-i-do-not-want-to-assign-a-cc-license/
/for-authors/what-is-a-cc-license/
/for-authors/what-we-do-to-clear-copyright-status-of-used-material/
/for-authors/which-cc-license-should-i-choose/
/for-authors/why-should-i-contribute-my-work/
/repository/ -> /about#repository
    """


    config.add_301(
        '/{year}/{month}/{day}/escidoc{id}/',
        lambda req: req.route_url(
            'source',
            id='item_{0}'.format(req.matchdict['id'].split('-')[0]),
            _query=req.query_params),
        name='item')
    config.add_301(
        '/category/iso639_3/{id}/',
        lambda req: req.route_url(
            'language',
            id=req.matchdict['id'].split('-')[0],
            _query=req.query_params),
        name='category')

    return config.make_wsgi_app()
