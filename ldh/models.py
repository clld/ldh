from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Source, Language, LanguageSource
from clld_glottologfamily_plugin.models import HasFamilyMixin, Family


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class LDHLanguage(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    macroarea = Column(Unicode)
    descriptions = relationship(Source, secondary=LanguageSource.__table__)


@implementer(interfaces.ISource)
class Description(CustomModelMixin, Source):
    pk = Column(Integer, ForeignKey('source.pk'), primary_key=True)
    pid = Column(Unicode)
    pid_type = Column(Unicode)

    @property
    def permalink_url(self):
        if self.pid_type == 'doi':
            return 'https://doi.org/{0.pid}'.format(self)
        return 'http://hdl.handle.net/{0.pid}'.format(self)

    @property
    def permalink_label(self):
        if self.pid_type == 'doi':
            return 'DOI: {0.pid}'.format(self)
        return 'hdl: {0.pid}'.format(self)
