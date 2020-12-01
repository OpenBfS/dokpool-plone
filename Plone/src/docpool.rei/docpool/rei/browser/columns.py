from collective.eeafaceted.z3ctable.columns import BaseColumn

from Products.CMFPlone.utils import safe_unicode
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from docpool.rei import DocpoolMessageFactory as _


def populate_a_tag(obj, link_title):
    """ Prepares the link """
    url = obj.absolute_url()
    return u'<a title="{0}" href={1}>{2}</a>'.format(safe_unicode(obj.Title()), url, safe_unicode(link_title))


class ReiReport(BaseColumn):
    """  """

    header = _('header_Title_ReiReport')
    sort_index = 'sortable_title'
    weight = 10

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        files = obj.getFiles()
        if not files:
            pdf_link = u''
        if files:
            title = files[0].title
            url = files[0].absolute_url()
            pdf_link = u'<a title="{0}" href={1}>PDF ansehen</a><br>'.format(safe_unicode(title), url)
        return pdf_link + u'<a title="{0}" href={1}>zum Dokument</a>'.format(safe_unicode(obj.Title()), obj.absolute_url())


class ReiLegalBases(BaseColumn):
    """  """

    header = _('header_Title_ReiLegalBases')
    sort_index = 'sortable_title'
    weight = 20

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return populate_a_tag(obj, ', '.join(obj.ReiLegalBases))

class Medium(BaseColumn):

    header = _('header_Title_Medium')
    sort_index = 'sortable_title'
    weight = 30

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return populate_a_tag(obj, obj.Medium)

class Authority(BaseColumn):
    """ """

    header = _('header_Title_Authority')
    sort_index = 'sortable_title'
    weight = 30

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.AuthorityVocabulary')()
        return populate_a_tag(obj, voc.getTerm(obj.Authority).title)


class NuclearInstallation(BaseColumn):

    header = _('header_Title_NuclearInstallation')
    sort_index = 'sortable_title'
    weight = 40

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.NuclearInstallationVocabulary')()
        installations = u', '.join(voc.getTerm(i).title for i in obj.NuclearInstallations)
        return populate_a_tag(obj, installations)


class Period(BaseColumn):

    header = _('header_Title_Period')
    sort_index = 'sortable_title'
    weight = 50

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        period_vocabulary = getUtility(IVocabularyFactory,
                                       'docpool.rei.vocabularies.PeriodVocabulary')()
        period = safe_unicode(period_vocabulary.getTerm(obj.Period).title)
        year = str(obj.Year)
        return populate_a_tag(obj, period + " " + year)


class Origin(BaseColumn):

    header = _('header_Title_Origin')
    sort_index = 'sortable_title'
    weight = 60

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return populate_a_tag(obj, ', '.join(obj.Origins))


class Metadata(BaseColumn):

    sort_index = None
    header = _('header_Title_Metadata')
    weight = 70

    def renderCell(self, item):
        obj_url = item.original_getURL()
        return u'<a href="#" class="pat-contentloader-bfs rei-eea-search open" data-pat-contentloader-bfs="url:{0}/@@meta?ajax=true;target:#target_{1}"><div title="Arrow up" >Open</div></a><div id="target_{2}"></div>'.format(obj_url, item.UID, item.UID)
