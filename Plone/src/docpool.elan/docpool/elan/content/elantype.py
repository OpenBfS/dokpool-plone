# -*- coding: utf-8 -*-
#
# File: elantype.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANType content type. See elantype.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Item
from docpool.base.content.doctypeextension import DocTypeExtension, IDocTypeExtension

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.base.utils import queryForObjects, queryForObject, back_references
from Products.Archetypes.utils import shasattr, DisplayList
from z3c.relationfield import RelationValue
from zope.intid import IIntIds
from zope.component import getUtility
from Acquisition import aq_inner
##/code-section imports 

from docpool.elan.config import PROJECTNAME

from docpool.elan import DocpoolMessageFactory as _

class IELANType(form.Schema, IDocTypeExtension):
    """
    """

##code-section interface
    contentCategory = RelationChoice(
        title=_(u'label_doctype_contentcategory', default=u'Choose category for this type '),
        description=_(u'description_doctype_contentcategory', default=u''),
        required=False,
        ##code-section field_contentCategory
        source="elan.esd.vocabularies.Category",
        ##/code-section field_contentCategory
    )


# form.widget(contentCategory=SelectWidget)
form.widget(contentCategory='z3c.form.browser.select.SelectFieldWidget')


@form.default_value(field=IELANType['contentCategory'])
def getDefaultCategory(data):
    """
    """
    if hasattr(data.context, "getDefaultCategory"):
        return data.context.getDefaultCategory()
    else:
        return None
##/code-section interface


class ELANType(Item, DocTypeExtension):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANType)
    
##code-section methods
    def __init__(self, context):
        self.context = context

    def _get_contentCategory(self):
        return self.context.contentCategory

    def _set_contentCategory(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.contentCategory = value

    contentCategory = property(_get_contentCategory, _set_contentCategory)

    def category(self):
        """
        The primary category that the documents of this type belong to.
        """
        cc = self.contentCategory
        res = cc and cc.to_object.title or ""
        return res

    def categories(self):
        """
        All categories, the document belongs to.
        """
        #         colls = self.getBackReferences(relationship='doctypes')
        colls = back_references(self, "docTypes")
        return list(set([coll.title for coll in colls if
                         coll and not coll.isArchive() and coll.getPortalTypeName() == 'ELANDocCollection']))

    def getCategories(self):
        """
        """
        mpath = "/"
        if shasattr(self, "dpSearchPath", acquire=True):
            mpath = self.dpSearchPath()
        ecs = queryForObjects(self, path=mpath, portal_type="ELANDocCollection", sort_on="sortable_title")
        return DisplayList([(ec.UID, ec.Title) for ec in ecs])

    def getDefaultCategory(self):
        """
        """
        #         colls = self.getBackReferences(relationship='doctypes')
        colls = self.back_references("docTypes")
        res = None
        if len(colls) == 1:  # Only when unique
            if colls[0]:
                intids = getUtility(IIntIds)
                to_id = intids.getId(colls[0])
                res = RelationValue(to_id)
                #         print 'getDefaultCategory ', res
        return res

    def setCCategory(self, id):
        """
        """
        mpath = "/"
        if shasattr(self, "dpSearchPath", acquire=True):
            mpath = self.dpSearchPath()
        o = queryForObject(self, path=mpath, portal_type="ELANDocCollection", id=id)
        #         print "CCategory", o
        intids = getUtility(IIntIds)
        to_id = intids.getId(o)
        self.contentCategory = RelationValue(to_id)

##/code-section methods 


##code-section bottom
##/code-section bottom 
