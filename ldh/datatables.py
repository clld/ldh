from sqlalchemy import desc
from clld.web.datatables.source import Sources


class Descriptions(Sources):
    def default_order(self):
        return desc(self.db_model().pk)


def includeme(config):
    config.register_datatable('sources', Descriptions)
