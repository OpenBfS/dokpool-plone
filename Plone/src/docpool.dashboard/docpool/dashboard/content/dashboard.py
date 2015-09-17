# -*- coding: utf-8 -*-
#
# File: dashboard.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Dashboard content type. See dashboard.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Item

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from docpool.dashboard.config import PROJECTNAME

from docpool.dashboard import ELAN_EMessageFactory as _

class IDashboard(form.Schema):
    """
    """
        
    dbCollections = RelationList(
                        title=_(u'label_dashboard_dbcollections', default=u'Document Types'),
                        description=_(u'description_dashboard_dbcollections', default=u'Select the document types you want to show in this dashboard.'),
                        required=False,
##code-section field_dbCollections
                        value_type=RelationChoice(
                                                      title=_("Document Types"),
                                                    source = "docpool.dashboard.vocabularies.DashboardCollections",

                                                     ),
##/code-section field_dbCollections                           
    )
    

##code-section interface
    form.widget(dbCollections='z3c.form.browser.select.CollectionSelectFieldWidget')
##/code-section interface


class Dashboard(Item):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDashboard)
    
##code-section methods
    def currentDocuments(self):
        """
        Loop through all configured collections,
        get the most recent document (if available).
        """
        res = []
        for c in self.dbCollections:
            coll = c.to_object
            docs = coll.results(b_size=1)
            if len(docs) > 0:
                res.append((coll.Title(), docs[0]))
            else:
                res.append((coll.Title(), None))
#        print res
        return res
            
##/code-section methods 


##code-section bottom
##/code-section bottom 
