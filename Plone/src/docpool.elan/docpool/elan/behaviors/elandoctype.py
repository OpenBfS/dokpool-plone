from Acquisition import aq_inner
from docpool.base.interfaces import IDocTypeExtension
from docpool.base.utils import back_references, queryForObject
from docpool.elan import DocpoolMessageFactory as _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from Products.CMFPlone.utils import safe_hasattr
from z3c.relationfield.relation import RelationValue
from z3c.relationfield.schema import RelationChoice
from zope.component import getUtility
from zope.interface import provider
from zope.intid.interfaces import IIntIds
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def getDefaultCategory(context):
    """ """
    # TODO: Does this make sense here?
    # Context is the container where the item is created...
    if hasattr(context, "getDefaultCategory"):
        return context.getDefaultCategory()
    else:
        return None


@provider(IFormFieldProvider)
class IELANDocType(IDocTypeExtension):
    contentCategory = RelationChoice(
        title=_(
            "label_doctype_contentcategory", default="Choose category for this type "
        ),
        description=_("description_doctype_contentcategory", default=""),
        required=False,
        # TODO: Why would we want a defaultFactory?
        # defaultFactory=getDefaultCategory,
        vocabulary="elan.esd.vocabularies.Category",
    )
    directives.widget(
        "contentCategory",
        SelectFieldWidget,
    )


class ELANDocType:
    def __init__(self, context):
        self.context = context

    def _get_contentCategory(self):
        return self.context.contentCategory

    def _set_contentCategory(self, value):
        context = aq_inner(self.context)
        context.contentCategory = value

    contentCategory = property(_get_contentCategory, _set_contentCategory)

    def category(self):
        """
        The primary category that the documents of this type belong to.
        """
        cc = self.context.contentCategory
        res = cc and cc.to_object.title or ""
        return res

    def categories(self):
        """
        All categories, the document belongs to.
        """
        #         colls = self.getBackReferences(relationship='doctypes')
        colls = back_references(self.context, "docTypes")
        return list(
            {
                coll.Title()
                for coll in colls
                if coll
                and not coll.restrictedTraverse("@@context_helpers").is_archive()
                and coll.getPortalTypeName() == "ELANDocCollection"
            }
        )

    def getDefaultCategory(self):
        """ """
        # TODO: does this make sense here?
        colls = self.context.back_references("docTypes")
        res = None
        if len(colls) == 1:  # Only when unique
            if colls[0]:
                intids = getUtility(IIntIds)
                to_id = intids.getId(colls[0])
                res = RelationValue(to_id)
                #         print 'getDefaultCategory ', res
        return res

    def setCCategory(self, id):
        """ """
        mpath = "/"
        if safe_hasattr(self.context, "dpSearchPath"):
            mpath = self.context.dpSearchPath()
        o = queryForObject(
            self.context, path=mpath, portal_type="ELANDocCollection", id=id
        )
        # print "CCategory", o
        intids = getUtility(IIntIds)
        to_id = intids.getId(o)
        self.context.contentCategory = RelationValue(to_id)
