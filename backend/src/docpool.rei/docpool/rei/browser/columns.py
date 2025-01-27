from collective.eeafaceted.z3ctable.columns import BaseColumn
from docpool.rei import DocpoolMessageFactory as _
from plone.base.utils import safe_text
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


def populate_a_tag(obj, link_title):
    """Prepares the link"""
    url = obj.absolute_url()
    return f'<a title="{safe_text(obj.Title())}" href={url}>{safe_text(link_title)}</a>'


class ReiReport(BaseColumn):
    """ """

    header = _("header_Title_ReiReport")
    sort_index = -1
    weight = 10
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        files = obj.getFiles()
        if not files:
            pdf_link = ""
        if files:
            title = files[0].title
            url = files[0].absolute_url()
            pdf_link = f'<a title="{safe_text(title)}" href={url} target="_blank">PDF ansehen</a><br>'
        return (
            pdf_link
            + f'<a title="{safe_text(obj.Title())}" href={obj.absolute_url()}>zum Dokument</a>'
        )


class ReiLegalBases(BaseColumn):
    """ """

    header = _("header_Title_ReiLegalBases")
    sort_index = -1
    weight = 20
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return populate_a_tag(obj, ", ".join(obj.ReiLegalBases))


class Medium(BaseColumn):
    header = _("header_Title_Medium")
    sort_index = -1
    weight = 30
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        # Todo Vocab should be updated and fixed via upgrade step
        try:
            if obj.Medium is None:
                return ""
            return populate_a_tag(obj, obj.Medium)
        except AttributeError:
            return ""


class Period(BaseColumn):
    header = _("header_Title_Period")
    sort_index = -1
    weight = 40
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        period_vocabulary = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.PeriodVocabulary"
        )(obj)
        period = safe_text(period_vocabulary.getTerm(obj.Period).title)
        year = str(obj.Year)
        return populate_a_tag(obj, period + " " + year)


class Authority(BaseColumn):
    """ """

    header = _("header_Title_Authority")
    sort_index = -1
    weight = 50
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.AuthorityVocabulary"
        )(obj)
        return populate_a_tag(obj, voc.getTerm(obj.Authority).title)


class NuclearInstallation(BaseColumn):
    header = _("header_Title_NuclearInstallation")
    sort_index = -1
    weight = 60
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.NuclearInstallationVocabulary"
        )(obj)
        installations = ", ".join(
            voc.getTerm(i).title for i in obj.NuclearInstallations
        )
        return populate_a_tag(obj, installations)


class Origin(BaseColumn):
    header = _("header_Title_Origin")
    sort_index = -1
    weight = 70
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        voc = getUtility(
            IVocabularyFactory, "docpool.rei.vocabularies.OriginVocabulary"
        )(obj)
        origins = ", ".join(voc.getTerm(i).title for i in obj.Origins)
        return populate_a_tag(obj, origins)


class Metadata(BaseColumn):
    header = _("header_Title_Metadata")
    sort_index = -1
    weight = 80
    escape = False

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        obj_url = item.original_getURL()
        title_html = '<a href="#" class="pat-contentloader-bfs rei-eea-search metatitle" data-pat-contentloader-bfs="content:#row_{0} .rei_title;target:#target_{0}"><div title="Titel auf- bzw. zuklappen" >Open</div></a><h4 class="rei_title" style="display:none">{1}</h4>'.format(
            item.UID, safe_text(obj.Title())
        )
        metadata_html = f'<a href="#" class="pat-contentloader-bfs rei-eea-search metadata" data-pat-contentloader-bfs="url:{obj_url}/@@meta?ajax=true;target:#target_{item.UID}"><div title="Metadaten auf- bzw. zuklappen" >Open</div></a><div id="target_{item.UID}"></div>'
        return title_html + metadata_html
