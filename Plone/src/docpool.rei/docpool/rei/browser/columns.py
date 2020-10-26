from collective.eeafaceted.z3ctable.columns import BaseColumn

from Products.CMFPlone.utils import safe_unicode

class ReiLegalBases(BaseColumn):
    """  """

    header = ('header_Title_ReiLegalBases')
    sort_index = 'sortable_title'
    weight = 0

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return ', '.join(obj.ReiLegalBases)

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
        return obj.NuclearInstallation


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
        import pdb; pdb.set_trace()
        return obj.Origins
