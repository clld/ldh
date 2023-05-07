from pyramid.config import Configurator
from clld.interfaces import IMapMarker, IDownload
from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

# we must make sure custom models are known at database initialization!
from ldh import models
from ldh import adapters

_ = lambda s: s
_('Source')
_('Sources')


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
/comments/feed/
/feed/ -> /sources.atom
    """
    config.add_301('/about/', lambda req: req.route_url('dataset', id='ldh'))
    config.add_301('/about/objective/', lambda req: req.route_url('about', _anchor='objectives'))
    config.add_301('/repository/', lambda req: req.route_url('about', _anchor='repository'))
    config.add_301('/archive/', lambda req: req.route_url('sources'))
    config.add_301('/category/iso639_3/', lambda req: req.route_url('languages'))
    config.add_301('/category/allgemein/', lambda req: req.route_url('languages'))
    config.add_301('/contact/', lambda req: req.route_url('contact'))
    config.add_301('/for-authors/', lambda req: req.route_url('help'))
    config.add_301('/for-authors/{path}/', lambda req: req.route_url('help'))
    config.add_301('/feed/', lambda req: req.route_url('sources_alt', ext='atom'))

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

    config.register_download(
        adapters.BibTeX(models.Description, 'ldh', description="Descriptions as BibTeX"))

    return config.make_wsgi_app()
