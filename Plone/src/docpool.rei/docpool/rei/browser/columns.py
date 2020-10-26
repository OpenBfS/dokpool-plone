from collective.eeafaceted.z3ctable.columns import BaseColumn

from Products.CMFPlone.utils import safe_unicode

class ReiLegalBases(BaseColumn):
    """  """

    header = ('header_Title_ReiLegalBases')
    sort_index = 'sortable_title'
    weight = 1000

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        dview_link = '{0}/@@dview?d={1}'.format(self.context.absolute_url(), obj.UID())
        return '<a href={0}>{1}</a>'.format(dview_link, ', '.join(obj.ReiLegalBases))

class Authority(BaseColumn):
    """ """

    header = ('header_Title_Authority')
    sort_index = 'sortable_title'
    weight = 100

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return obj.Authority

class NuclearInstallation(BaseColumn):

    header = ('header_Title_NuclearInstallation')
    sort_index = 'sortable_title'
    weight = 200

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return ', '.join(obj.NuclearInstallations)


class Period(BaseColumn):

    header = ('header_Title_Period')
    sort_index = 'sortable_title'
    weight = 300

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return obj.Period


class Origin(BaseColumn):

    header = ('header_Title_Origin')
    sort_index = 'sortable_title'
    weight = 400

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return ', '.join(obj.Origins)
