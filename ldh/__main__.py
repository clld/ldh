import sys
import json

from clldutils.clilib import ArgumentParserWithLogging, command

from ldh import pure
from ldh.util import get, REPOS, bs, iter_posts


@command()
def crawl_ldh(args):
    def read_post(url, pid):
        doc = bs(get(url))
        article = doc.find('article', id=pid)
        if not article:
            print('--- missing:', url)
            return
        p = article.find('p')
        link = p.find('a')
        if link.text != '[PuRe Item]':
            print('--- missing PuRe link:', url, link.text)
            return
        return dict(url=link['href'], html='{0}'.format(article))

    def iter_posts():
        seen = set()
        for a in bs(get("http://ldh.clld.org/archive")).find_all('a', href=True, class_=True):
            if a['class'][0].startswith('post') and a['href'].startswith('http://ldh'):
                if a['href'] not in seen:
                    yield a['href'], a['class'][0]
                    seen.add(a['href'])

    posts = {}
    for i, (url, pid) in enumerate(iter_posts()):
        posts[url] = [pid, read_post(url, pid)]
    with REPOS.joinpath('posts.json').open('w') as fp:
        json.dump(posts, fp, indent=4)


@command()
def crawl_pure(args):
    out = REPOS.joinpath('json')
    for post in iter_posts():
        if post.pure_item_id:
            out.joinpath(post.pure_item_id + '.json').write_text(
                get('https://pure.mpg.de/rest/items/' + post.pure_item_id), encoding='utf8')
    return


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
