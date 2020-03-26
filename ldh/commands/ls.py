"""

"""
from ldh import pure
from ldh.util import iter_posts


def run(args):
    for post in iter_posts():
        if post.pure_item_id:
            item = pure.Item.from_json(post.pure_item_id)
            print(item.as_source().bibtex())
