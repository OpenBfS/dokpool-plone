# -*- coding: utf-8 -*-
#
# File: irixreport.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the IRIXReport content type. See irixreport.py for more
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
from docpool.base.content.contentbase import ContentBase, IContentBase

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.dbaccess.dbinit import __metadata__, __session__

metadata = __metadata__
session = __session__

from zope.component import adapter
from zope.component import getUtility
from docpool.dbaccess.interfaces import Idbadmin
from zope.lifecycleevent import IObjectAddedEvent, IObjectRemovedEvent
from elan.irix.db.model import IRIXReport as DBReport
from datetime import datetime
from urllib import quote
##/code-section imports 

from elan.irix.config import PROJECTNAME

from elan.irix import DocpoolMessageFactory as _

class IIRIXReport(form.Schema, IContentBase):
    """
    """
        
    dbkey = schema.Decimal(
                        title=_(u'label_irixreport_dbkey', default=u'Primary key in relational database'),
                        description=_(u'description_irixreport_dbkey', default=u'Database key'),
                        required=False,
##code-section field_dbkey
##/code-section field_dbkey                           
    )
    form.omitted('dbkey')

##code-section interface
##/code-section interface


class IRIXReport(Item, ContentBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IIRIXReport)
    
##code-section methods
    def pkfields(self):
        """
        Dummy for CSS
        """
        pass

    def getStructuredType(self):
        """
        """
        return "irixreport"
    
    def getPrimaryKey(self):
        """
        """
        return [self.dbkey]
    
    def dbObj(self):
        """
        """
        dba = getUtility(Idbadmin)
        pk = self.getPrimaryKey()
        pkvals = dba.getPKDict(self.getStructuredType(), pk)
        # print pkvals
        obj = dba.objektdatensatz(self.getStructuredType(), **pkvals)
        return obj
        
    def navigationHTML(self):
        """
        """
        obj = self.dbObj()
        os = obj.getSubObjects()
        html = self.navElement(os)
        return html
        
    def navElement(self, el):
        """
        """
        typ, pk, bc = self.currentState()
        mytyp = el[1]
        mypk = eval(el[2])
        
        currentLeaf = False
        currentNode = False
        if typ == el[1]:
            if list(pk) == mypk:
                currentLeaf = True
        else:
            for b in bc:
                if mytyp == b[0]:
                    if mypk == list(b[1]):
                        currentNode = True
        html = ''
        anchor_class = currentLeaf and 'currentLeaf' or currentNode and 'currentNode' or 'normal'
        css_class = 'node'
        if el[4]:
            css_class = 'node content'
        html += "<li class='%s'>" % css_class
        html += "<a class='%s' href='%s/struct_edit?typ=%s&pk=%s&bc=%s'>%s</a>" % (anchor_class, self.absolute_url(), el[1], quote(el[2]), quote(el[3]), el[0])
        if el[4]:
            html += "<ul class='folder'>"
            for subel in el[4]:
                html += self.navElement(subel)
            html += "</ul>"
        html += "</li>"
        return html
        
    def currentState(self):
        """
        """
        request = self.REQUEST
        typ = request.get("typ", None)
        pk = eval(request.get("pk", '[]'))
        bc = eval(request.get("bc", '[]'))
        return typ, pk, bc
    
    def initializeDB(self):
        """
        """
        # TODO: IRIXReport DB object with default data acquired from IRIX config
        ic = self.irixConfig()
        dbReport = DBReport()
        dbReport.title = self.Title()
        dbReport.UUID = self.UID()
        dbReport.OrganisationReporting = ic.organisationReporting
        dbReport.DatetimeOfSubmittal = datetime.now()
        dbReport.ReportContext = "TBD"
        dbReport.Confidentiality = "TBD"
        dbReport.Name = ic.contactName
        dbReport.OrganisationID = ic.organisationId
        dbReport.Country = ic.organisationCountry
        dbReport.EmailAddress = ic.organisationEmail
        dbReport.WebAddress = ic.organisationWeb
        dbReport.Name = ic.organisationName
        __session__.add(dbReport)
        __session__.flush()
        self.dbkey = dbReport.id
        # print self.dbkey
        self.reindexObject()
        # store PK
        
    def irixConfig(self):
        try:
            ic = self.contentconfig.irix
            return ic
        except:
            return None
            
##/code-section methods 


##code-section bottom
@adapter(IIRIXReport, IObjectAddedEvent)
def reportAdded(obj, event=None):
    """
    """
    obj.initializeDB()
    obj.reindexObject()

@adapter(IIRIXReport, IObjectRemovedEvent)
def reportRemoved(obj, event=None):
    """
    """
    obj.deleteData()
##/code-section bottom 
