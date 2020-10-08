from collective.eeafaceted.z3ctable.columns import BaseColumn

from Products.CMFPlone.utils import safe_unicode

class Netzbetreiber(BaseColumn):
    """ Just POC needs real data """

    header = ('header_Title_bfs')
    sort_index = 'sortable_title'
    weight = 1000

    def renderCell(self, item):
        value = self.getValue(item)
        if not value:
            value = u'-'
        value = safe_unicode(value)
        return u'<a href="{0}">{1}</a>'.format(item.getURL(), value)