from collective.eeafaceted.z3ctable.columns import BaseColumn

from Products.CMFPlone.utils import safe_unicode

class ReiLegalBases(BaseColumn):
    """ Just POC needs real data """

    header = ('header_Title_ReiLegalBases')
    sort_index = 'sortable_title'
    weight = 0

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return ', '.join(obj.ReiLegalBases)

class Authority(BaseColumn):
    """ Just POC needs real data """

    header = ('header_Title_Authority')
    sort_index = 'sortable_title'
    weight = 100

    def renderCell(self, item):
        obj = self._getObject(item)
        if not obj:
            return
        return obj.Authority
