import sys
import json

from clldutils.clilib import ArgumentParserWithLogging, command

from ldh import pure
from ldh import zenodo
from ldh.util import get, REPOS, bs, iter_posts


@command()
def crawl_zenodo(args):
    zenodo.crawl()


@command()
def items(args):
    for post in iter_posts():
        if post.pure_item_id:
            item = pure.Item.from_json(post.pure_item_id)
            #print(item.authors, item.creators, item.title)
            print(item.as_source().bibtex())


def main():  # pragma: no cover
    parser = ArgumentParserWithLogging('ldh')
    sys.exit(parser.main())


if __name__ == '__main__':
    main()
