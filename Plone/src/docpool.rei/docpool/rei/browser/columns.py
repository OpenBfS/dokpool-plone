from collective.eeafaceted.z3ctable.columns import BaseColumn

from Products.CMFPlone.utils import safe_unicode
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from docpool.rei import DocpoolMessageFactory as _

CELL_LINK = u'<a title={0} href={1}>{2}</a>'

class ReiLegalBases(BaseColumn):
    """  """

    header = _('header_Title_ReiLegalBases')
    sort_index = 'sortable_title'
    weight = 1

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return CELL_LINK.format(safe_unicode(obj.title), obj.absolute_url(), ', '.join(obj.ReiLegalBases))


class Authority(BaseColumn):
    """ """

    header = _('header_Title_Authority')
    sort_index = 'sortable_title'
    weight = 2

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.AuthorityVocabulary')()
        return CELL_LINK.format(safe_unicode(obj.title), obj.absolute_url(), voc.getTerm(obj.Authority).title)


class NuclearInstallation(BaseColumn):

    header = _('header_Title_NuclearInstallation')
    sort_index = 'sortable_title'
    weight = 3

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.NuclearInstallationVocabulary')()
        return u', '.join(voc.getTerm(i).title for i in obj.NuclearInstallations)


class Period(BaseColumn):

    header = _('header_Title_Period')
    sort_index = 'sortable_title'
    weight = 4

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        period_vocabulary = getUtility(IVocabularyFactory,
                                       'docpool.rei.vocabularies.PeriodVocabulary')()
        return period_vocabulary.getTerm(obj.Period).title


class Origin(BaseColumn):

    header = _('header_Title_Origin')
    sort_index = 'sortable_title'
    weight = 10

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return ', '.join(obj.Origins)


class Metadata(BaseColumn):

    sort_index = None
    header = _('header_Title_Metadata')
    weight = 20

    def renderCell(self, item):
        obj_url = item.original_getURL()
        return u'<a href="#" class="pat-contentloader" data-pat-contentloader="url:something.html;"><img src="{1}/++theme++docpoolrei/arrow_down_open.png" title="Arrow up" /></a>'.format(obj_url, self.table.portal_url)
