# -*- coding: utf-8 -*-
#
# File: dptransferfolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DPTransferFolder content type. See dptransferfolder.py for more
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

from plone.dexterity.content import Container
from docpool.base.content.folderbase import FolderBase, IFolderBase

from Products.CMFCore.utils import getToolByName

##code-section imports
from zope.interface import Interface
from zope.schema.interfaces import IContextSourceBinder
from docpool.base.utils import execute_under_special_role, queryForObject, getDocumentPoolSite
from zope.component.hooks import getSite
from zope.component import adapter
from plone.formwidget.autocomplete.widget import AutocompleteFieldWidget
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow
from Products.Archetypes.utils import shasattr
from zope.lifecycleevent.interfaces import IObjectAddedEvent,\
    IObjectRemovedEvent
from plone.dexterity.interfaces import IEditFinishedEvent
from docpool.dbaccess.dbinit import __metadata__, __session__
from docpool.transfers.db.model import Channel, DocTypePermission, ChannelPermissions
from logging import getLogger
from Products.CMFPlone.utils import parent


from docpool.transfers import DocpoolMessageFactory as _
logger = getLogger("dptransferfolder")

##/code-section imports

from docpool.transfers.config import PROJECTNAME

class IDPTransferFolder(form.Schema, IFolderBase):
    """
    """
        
    sendingESD = schema.Choice(
                        title=_(u'label_dptransferfolder_sendingesd', default=u'The organisation sending content via this transfer folder'),
                        description=_(u'description_dptransferfolder_sendingesd', default=u''),
                        required=True,
##code-section field_sendingESD
                        source = "docpool.base.vocabularies.DocumentPools",
##/code-section field_sendingESD                           
    )
    
        
    permLevel = schema.Choice(
                        title=_(u'label_dptransferfolder_permlevel', default=u'Permission level'),
                        description=_(u'description_dptransferfolder_permlevel', default=u''),
                        required=True,
                        default="read/write",
##code-section field_permLevel
                        source="docpool.transfers.vocabularies.Permissions"
##/code-section field_permLevel                           
    )
    
        
    unknownDtDefault = schema.Choice(
                        title=_(u'label_dptransferfolder_unknowndtdefault', default=u'Default for unknown document types'),
                        description=_(u'description_dptransferfolder_unknowndtdefault', default=u''),
                        required=True,
                        default="block",
##code-section field_unknownDtDefault
                        source="docpool.transfers.vocabularies.UnknownOptions"
##/code-section field_unknownDtDefault                           
    )
    
        
    unknownScenDefault = schema.Choice(
                        title=_(u'label_dptransferfolder_unknownscendefault', default=u'Default for unknown scenarios'),
                        description=_(u'description_dptransferfolder_unknownscendefault', default=u''),
                        required=True,
                        default="block",
##code-section field_unknownScenDefault
                        source="docpool.transfers.vocabularies.UnknownOptions"
##/code-section field_unknownScenDefault                           
    )
    

##code-section interface
#    form.widget(typesConf=DataGridFieldFactory)
##/code-section interface


class DPTransferFolder(Container, FolderBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDPTransferFolder)
    
##code-section methods
    def migrate(self):
        f = parent(self)
        if hasattr(self, '_setPortalTypeName'):
            self._setPortalTypeName("DPTransfers")
        myid = self.getId()
        del f[myid]
        self.__class__ = DPTransferFolder
        f[myid] = self
        logger.info(self.__class__)
        logger.info(self.getPortalTypeName())

    def acceptsDT(self, dt_id):
        """
        Do I specifically accept this doc type?
        """
        channel_id = self.channelId()
        perm = __session__.query(DocTypePermission).filter_by(channel_id=channel_id,doc_type=dt_id).all()
        if perm:
            if perm[0].perm != 'block':
                return True
            else:
                return False
        else:
            return False

    def getMatchingDocumentTypes(self, ids_only=True):
        """
        """
        def doIt():
            esd = self.getSendingESD()
            theirDts = esd.myDocumentTypes(ids_only=True)
            myDts = self.myDocumentTypes()
            #print theirDts
            #print myDts
            if ids_only:
                return [ dt[0] for dt in myDts if dt[0] in theirDts]
            else:    
                return [ dt for dt in myDts if dt[0] in theirDts]
        return execute_under_special_role(self, "Manager",doIt)
    
    def ensureMatchingDocumentTypesInDatabase(self):
        """
        """
        #print "ensureMatching"
        channel_id = self.channelId()
        dts = self.getMatchingDocumentTypes(ids_only=True)
        #print dts
        # first delete
        permissions = self.permissions()
        dbdts = [ perm.doc_type for perm in permissions]
        for perm in permissions:
            if perm.doc_type not in dts:
                __session__.delete(perm)
        for dt in dts:
            if dt not in dbdts:
                p = DocTypePermission(doc_type=dt,perm="publish",channel_id=channel_id)
        __session__.flush()        
    
    def getSendingESD(self):
        """
        """
        esd_uid = self.sendingESD
        return queryForObject(self, UID=esd_uid)
    
    def resetSettings(self):
        """
        """
        created(self, event=None)
        
    def permissions(self):
        """
        """
        channel_id = self.channelId()
        permissions = __session__.query(DocTypePermission).filter_by(channel_id=channel_id).order_by(DocTypePermission.doc_type).all()
        return permissions
    
    def channelId(self):
        """
        """
        esd_from_uid=self.sendingESD
        tf_uid=self.UID()
        channel = Channel.get_by(esd_from_uid=esd_from_uid,tf_uid=tf_uid)
        if channel:
            return channel.id
        else:
            return 0
        
    def pkfields(self):
        """
        Dummy method to indicate that this is a resource with dbadmin functions.
        """
        pass
    
    def grantReadAccess(self):
        """
        """
        def grantRead():
            esd = self.getSendingESD()
            prefix = esd.myPrefix()
            esd_members = "%s_Senders" % prefix
            self.myDocumentPool().manage_setLocalRoles(esd_members, ["Reader"])
            self.myDocumentPool().reindexObject()
            self.myDocumentPool().reindexObjectSecurity()

        execute_under_special_role(self, "Manager", grantRead)
        
    def revokeReadAccess(self):
        """
        """
        def revokeRead():
            esd = self.getSendingESD()
            if esd:
                prefix = esd.myPrefix()
                esd_members = "%s_Senders" % prefix
                self.myDocumentPool().manage_delLocalRoles([esd_members])
                self.myDocumentPool().reindexObject()
                self.myDocumentPool().reindexObjectSecurity()
            
        execute_under_special_role(self, "Manager", revokeRead)
    
    def isArchive(self):
        return "archive" in self.getPhysicalPath()        
##/code-section methods 

    def myDPTransferFolder(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getDPDocuments(self, **kwargs):
        """
        """
        args = {'portal_type':'DPDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getFiles(self, **kwargs):
        """
        """
        args = {'portal_type':'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type':'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getSRModules(self, **kwargs):
        """
        """
        args = {'portal_type':'SRModule'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getSituationReports(self, **kwargs):
        """
        """
        args = {'portal_type':'SituationReport'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom

def setupChannel(obj, delete=False):
    esd_from_uid=obj.sendingESD
    tf_uid=obj.UID()
    old = Channel.get_by(esd_from_uid=esd_from_uid, tf_uid=tf_uid)
    if old and delete:
        __session__.delete(old)

    if not old or delete:
        esd = obj.myDocumentPool()
        cat = getToolByName(obj, 'portal_catalog')
        from_esd = cat.unrestrictedSearchResults({"portal_type":"DocumentPool", "UID" : esd_from_uid})
        from_esd = from_esd[0]    
        dts = obj.getMatchingDocumentTypes(ids_only=True)
        c = Channel(esd_from_uid=esd_from_uid, esd_from_title=from_esd.Title, tf_uid=tf_uid, title=obj.Title(), esd_to_title=esd.Title())
        for dt in dts:
            p = DocTypePermission(doc_type=dt,perm="publish",channel=c)
        __session__.flush()
    else:
        c = old
    return c

@adapter(IDPTransferFolder, IObjectAddedEvent)
def created(obj, event=None):
    # Initialize all channel settings in the database.
    # For all document types shared between the two ESDs
    # set the default to "publish"
    log("TransferFolder created: %s" % str(obj))
    if not obj.isArchive():
        setupChannel(obj, delete=True)
    
        # Also, if the permissions include read access,
        # set the local Reader role for the members of
        # the sending ESD
        if obj.permLevel == 'read/write':
            obj.grantReadAccess()

@adapter(IDPTransferFolder, IEditFinishedEvent)
def updated(obj, event=None):
    # Actually, a transfer folder should never allow a change of ESD.
    # But the permission level could have been changed. So we adapt
    # the read permissions for the sending ESD accordingly.
    log("TransferFolder updated: %s" % str(obj))

    if not obj.isArchive():
        setupChannel(obj, delete=False)
    
        if obj.permLevel == 'read/write':
            obj.grantReadAccess()
        else:
            obj.revokeReadAccess()

@adapter(IDPTransferFolder, IObjectRemovedEvent)
def deleted(obj, event=None):
    # Delete all channel settings from the database.
    log("TransferFolder deleted: %s" % str(obj))
    if not obj.isArchive():
        esd_from_uid=obj.sendingESD
        tf_uid=obj.UID()    
        old = Channel.get_by(esd_from_uid=esd_from_uid, tf_uid=tf_uid)
        permissions = obj.permissions()
        for perm in permissions:
            __session__.delete(perm)
        __session__.flush()    
        if old:
            __session__.delete(old)
            __session__.flush()    
        # Revoke any read access
        obj.revokeReadAccess()

class ELANTransferFolder(DPTransferFolder):
    pass
##/code-section bottom 
