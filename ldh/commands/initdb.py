"""

"""
import pathlib
import contextlib

import transaction
from clldutils import db
from clldutils import clilib
from clld.scripts.util import SessionContext, ExistingConfig, get_env_and_settings
from cldfcatalog import Catalog

import ldh
from ldh.scripts.initializedb import main

PROJECT_DIR = pathlib.Path(ldh.__file__).parent.parent


def register(parser):
    parser.add_argument(
        "--config-uri",
        action=ExistingConfig,
        help="ini file providing app config",
        default=str(PROJECT_DIR / 'development.ini'))
    parser.add_argument(
        '--glottolog',
        type=clilib.PathType(type='dir'),
        help='glottolog/glottolog',
        default=PROJECT_DIR / '..' / '..' / 'glottolog' / 'glottolog',
    )
    parser.add_argument(
        '--glottolog-version',
        default=None,
    )


def run(args):
    args.env, settings = get_env_and_settings(args.config_uri)

    with contextlib.ExitStack() as stack:
        stack.enter_context(db.FreshDB.from_settings(settings, log=args.log))
        stack.enter_context(SessionContext(settings))
        stack.enter_context(Catalog(args.glottolog, tag=args.glottolog_version))

        with transaction.manager:
            main(args)
