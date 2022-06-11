from collective.eeafaceted.z3ctable.columns import BaseColumn
from docpool.rei import DocpoolMessageFactory as _
from plone.base.utils import safe_text
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility


def populate_a_tag(obj, link_title):
    """ Prepares the link """
    url = obj.absolute_url()
    return u'<a title="{0}" href={1}>{2}</a>'.format(safe_text(obj.Title()), url, safe_text(link_title))


class ReiReport(BaseColumn):
    """  """

    header = _('header_Title_ReiReport')
    sort_index = -1
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
            pdf_link = u'<a title="{0}" href={1} target="_blank">PDF ansehen</a><br>'.format(safe_text(title), url)
        return pdf_link + u'<a title="{0}" href={1}>zum Dokument</a>'.format(safe_text(obj.Title()), obj.absolute_url())


class ReiLegalBases(BaseColumn):
    """  """

    header = _('header_Title_ReiLegalBases')
    sort_index = -1
    weight = 20

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return populate_a_tag(obj, ', '.join(obj.ReiLegalBases))


class Medium(BaseColumn):

    header = _('header_Title_Medium')
    sort_index = -1
    weight = 30

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        # Todo Vocab should be updated and fixed via upgrade step
        try:
            if obj.Medium is None:
                return ''
            return populate_a_tag(obj, obj.Medium)
        except AttributeError:
            return ''


class Period(BaseColumn):

    header = _('header_Title_Period')
    sort_index = -1
    weight = 40

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        period_vocabulary = getUtility(IVocabularyFactory,
                                       'docpool.rei.vocabularies.PeriodVocabulary')()
        period = safe_text(period_vocabulary.getTerm(obj.Period).title)
        year = str(obj.Year)
        return populate_a_tag(obj, period + " " + year)


class Authority(BaseColumn):
    """ """

    header = _('header_Title_Authority')
    sort_index = -1
    weight = 50

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.AuthorityVocabulary')()
        return populate_a_tag(obj, voc.getTerm(obj.Authority).title)


class NuclearInstallation(BaseColumn):

    header = _('header_Title_NuclearInstallation')
    sort_index = -1
    weight = 60

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(IVocabularyFactory, 'docpool.rei.vocabularies.NuclearInstallationVocabulary')()
        installations = u', '.join(voc.getTerm(i).title for i in obj.NuclearInstallations)
        return populate_a_tag(obj, installations)


class Origin(BaseColumn):

    header = _('header_Title_Origin')
    sort_index = -1
    weight = 70

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return populate_a_tag(obj, ', '.join(obj.Origins))


class Metadata(BaseColumn):

    header = _('header_Title_Metadata')
    sort_index = -1
    weight = 80

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        obj_url = item.original_getURL()
        title_html = u'<a href="#" class="pat-contentloader-bfs rei-eea-search metatitle" data-pat-contentloader-bfs="content:#row_{0} .rei_title;target:#target_{0}"><div title="Titel auf- bzw. zuklappen" >Open</div></a><h4 class="rei_title" style="display:none">{1}</h4>'.format(item.UID, safe_text(obj.Title()))
        metadata_html = u'<a href="#" class="pat-contentloader-bfs rei-eea-search metadata" data-pat-contentloader-bfs="url:{0}/@@meta?ajax=true;target:#target_{1}"><div title="Metadaten auf- bzw. zuklappen" >Open</div></a><div id="target_{2}"></div>'.format(obj_url, item.UID, item.UID)
        return title_html + metadata_html