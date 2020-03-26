"""
Harvest data from the LDH community on Zenodo
"""
from ldh import zenodo


def run(args):
    zenodo.crawl()
