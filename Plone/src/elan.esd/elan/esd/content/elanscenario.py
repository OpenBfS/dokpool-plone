# -*- coding: utf-8 -*-
#
# File: elanscenario.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#
from docpool.base.structures import navSettings

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANScenario content type. See elanscenario.py for more
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
from docpool.base.content.contentbase import ContentBase, IContentBase

from Products.CMFCore.utils import getToolByName

##code-section imports
from DateTime import DateTime
from elan.policy.utils import TYPE, TITLE, ID, CHILDREN, DOCTYPES, createPloneObjects, ploneId
from Products.CMFPlone.utils import parent
from Products.CMFPlone.utils import log
from docpool.base.utils import portalMessage
from zope.component import getMultiAdapter
from Products.Archetypes.utils import DisplayList
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectMovedEvent, IObjectRemovedEvent, IObjectModifiedEvent
from Products.CMFCore.interfaces import IActionSucceededEvent
from elan.esd import ELAN_EMessageFactory
from Products.CMFPlone.i18nl10n import utranslate
import datetime
from five import grok
from zope.schema.interfaces import IContextSourceBinder

@grok.provider(IContextSourceBinder)
def availableScenarios(context):
    if hasattr(context, "dpSearchPath"):
        path = context.dpSearchPath() + "/contentconfig/scen"
    else:
        path = "/Plone/contentconfig/scen"
    query = { "portal_type" : ["ELANScenario"],
              "path": {'query' :path } 
             }

    return ObjPathSourceBinder(navigation_tree_query = query,object_provides=IELANScenario.__identifier__).__call__(context) 
##/code-section imports 

from elan.esd.config import PROJECTNAME

from elan.esd import ELAN_EMessageFactory as _

class IELANScenario(form.Schema, IContentBase):
    """
    """
        
    status = schema.Choice(
                        title=_(u'label_elanscenario_status', default=u'Status of the scenario'),
                        description=_(u'description_elanscenario_status', default=u''),
                        required=True,
##code-section field_status
                        source="docpool.base.vocabularies.Status",
##/code-section field_status                           
    )
    
        
    exercise = schema.Bool(
                        title=_(u'label_elanscenario_exercise', default=u'Is this an exercise?'),
                        description=_(u'description_elanscenario_exercise', default=u''),
                        required=False,
##code-section field_exercise
##/code-section field_exercise                           
    )
    
        
    timeOfEvent = schema.Datetime(
                        title=_(u'label_elanscenario_timeofevent', default=u'Time of event'),
                        description=_(u'description_elanscenario_timeofevent', default=u''),
                        required=True,
##code-section field_timeOfEvent
##/code-section field_timeOfEvent                           
    )
    
        
    substitute = RelationChoice(
                        title=_(u'label_elanscenario_substitute', default=u'Substitute scenario'),
                        description=_(u'description_elanscenario_substitute', default=u'Only relevant for private scenarios received from another organisation. Allows you map content for this scenario to one of you own scenarios.'),
                        required=False,
##code-section field_substitute
                        source="elan.esd.vocabularies.ScenarioSubstitutes"
##/code-section field_substitute                           
    )
    

##code-section interface
    form.widget(substitute='z3c.form.browser.select.SelectFieldWidget')
@form.default_value(field=IELANScenario['timeOfEvent'])
def initializeTimeOfEvent(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today()   
##/code-section interface


class ELANScenario(Item, ContentBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANScenario)
    
##code-section methods
    def getStates(self):
        """
        """
        return DisplayList([('active', _('active')),('inactive', _('inactive')),('closed', _('closed'))])

    def dp_type(self):
        """
        We reuse the dp_type index for the scenario status.
        """
        return self.status
    
    def purgeConfirmMsg(self):
        """
        Do you really want to remove all documents from this scenario?
        """
        return utranslate("elan.esd", "purge_confirm_msg", context=self)
    
    def archiveConfirmMsg(self):
        """
        Do you really want to archive this scenario?
        """
        return utranslate("elan.esd", "archive_confirm_msg", context=self)

    security.declareProtected("Modify portal content", "archiveAndClose")
    def archiveAndClose(self, REQUEST):
        """
        Saves all content for this scenario to an archive, deletes the original content,
        and sets the scenario to state "closed".
        """
        self.snapshot()
        self.purge()
        self.status='closed'
        self.reindexObject()
        portalMessage(self, _("Scenario archived"), "info")
        return self.restrictedTraverse("view")()
        
    security.declareProtected("Modify portal content", "snapshot")
    def snapshot(self, REQUEST=None):
        """
        Saves all content for this scenario to a new archive, but does not delete any files.
        Status is unchanged.
        """
        arc = self._createArchiveFolders()
        # TODO
        m = self.getELANContentAreas()[0]
        mpath = "/".join(m.getPhysicalPath())
        arc_m = arc.content
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        mdocs = self._getDocumentsForScenario(path=mpath)
        for doc in mdocs:
            target_folder = self._ensureTargetFolder(doc, arc_m)
            self._copyDocument(target_folder, doc)
        if REQUEST:
            portalMessage(self, _("Snapshot created"), "info")
            return self.restrictedTraverse("view")()
        
    def _ensureTargetFolder(self, doc, aroot):
        """
        Make sure that a personal or group folder with proper permissions
        exists for this document in the archive.
        """
        # 1. check whether this is a personal or a group document
        path = doc.getPath().split("/")
        isGroup = "Groups" in path
        if isGroup:
            aroot = aroot.Groups
        isTransfer = "Transfers" in path
        if isTransfer:
            aroot = aroot.Transfers
        isMember = "Members" in path
        if isMember:
            aroot = aroot.Members
        # 2. check for which user / group
        if len(path) >= 4:
            if isGroup or isTransfer or isMember:
                fname = path[5]
            else:
                fname = path[4]
        # 3. check for corresponding folder
        hasFolder = aroot.hasObject(fname)
        # 4. if it doesn't exist: create it
        if not hasFolder:
            print aroot
            folderType = "ELANFolder"
            if isTransfer:
                folderType = "ELANTransferFolder"
            aroot.invokeFactory(folderType, id=fname) # if not we create a new folder
        af = aroot._getOb(fname)
        # 5. and copy the local roles
        mroot = self.content.Members
        if isGroup:
            mroot = self.content.Groups
        if isTransfer:
            mroot = self.content.Transfers
        mf = mroot._getOb(fname)
        af.setTitle(mf.Title())
        if not isTransfer:
            mtool = getToolByName(self, "portal_membership")
            mtool.setLocalRoles(af,[fname],'Owner')
        af.reindexObject()
        af.reindexObjectSecurity()
        return af
        

    def _copyDocument(self, target_folder_obj, source_brain):
        """
        Copy utility
        """
        #TODO: transferLog fuellen und DB Eintraege loeschen
        # print source_brain.getId
        source_obj = source_brain.getObject()
        # determine parent folder for copy
        p = parent(source_obj)
        #if source_obj.getId() == 'ifinprojection.2012-08-08.4378013443':
        #    p._delOb('ifinprojection.2012-08-08.4378013443')
        #    return
        cb_copy_data = p.manage_copyObjects(source_obj.getId())
        result = target_folder_obj.manage_pasteObjects(cb_copy_data)
        # Now do some repairs
        if len(result) == 1:
            new_id = result[0]['new_id']
            copied_obj = target_folder_obj._getOb(new_id)
            mdate = source_obj.modified()
            copied_obj.scenarios=[]
            wf_state = source_brain.review_state
            wftool = getToolByName(self, 'portal_workflow')
            #print wf_state, wftool.getInfoFor(copied_obj, 'review_state')
            if wf_state == "published" and wftool.getInfoFor(copied_obj, 'review_state') != 'published':
                wftool.doActionFor(copied_obj, 'publish')
            copied_obj.setModificationDate(mdate)
            events = source_obj.transferEvents()
            copied_obj.transferLog = str(events)
            copied_obj.reindexObject()
            copied_obj.reindexObjectSecurity()
        else:
            log("Could not archive %s" % source_obj.absolute_url())

    def _getDocumentsForScenario(self, **kwargs):
        """
        Helper function for catalog queries
        """
        args = {'portal_type':'DPDocument', 'scenarios': self.getId()}
        args.update(kwargs)
        cat = getToolByName(self, "portal_catalog")
        return cat(args) 
        
    def _createArchiveFolders(self):
        """
        We create an archive object. Into it, we copy the complete ESD hierarchy. 
        We also create two folders "Members" and "Groups", which will hold all the
        documents for the scenario.
        """
        a = self.archive # Acquire root for archives
        e = self.esd # Acquire esd root
        now = self.toLocalizedTime(DateTime(), long_format=1)
        id = ploneId(self, "%s_%s" % (self.getId(), now))
        title = "%s %s" % (self.Title(), now)
        # create the archive root
        a.invokeFactory(id=id, type_name="ELANArchive", title=title)
        arc = a._getOb(id) # get new empty archive
        arc.setDescription(self.Description())
        # create the document folders
        f = [
             {TYPE: 'ELANCurrentSituation', TITLE: _('Electronic Situation Display'), ID: 'esd', CHILDREN: [
                  {TYPE: 'ELANDocCollection', TITLE: _('Overview'), ID: 'overview', "setExcludeFromNav": True, DOCTYPES: [], CHILDREN: [] },                                                                                                          
             
             ]},    
             {TYPE: 'ELANContentArea', TITLE: u'Content Area', ID: 'content', "setExcludeFromNav": True, CHILDREN: [
                 {TYPE: 'ELANUsers', TITLE: u'Members', ID: 'Members', CHILDREN: []},                                                                                              
                 {TYPE: 'ELANGroups', TITLE: u'Groups', ID: 'Groups', CHILDREN: []},                                                                                              
                 {TYPE: 'ELANTransfers', TITLE: u'Transfers', ID: 'Transfers', CHILDREN: []},                                                                                                                                                                                            
             ]},
        ]
        createPloneObjects(arc, f)
        
        navSettings(arc)

        arc.esd.setDefaultPage("overview")
        # copy the ESD folders
        objs = [o.getId for o in e.getFolderContents({'portal_type': ['ELANSection', 'ELANDocCollection']})]
        # print objs
        cb_copy_data = e.manage_copyObjects(objs) # Copy aus der Quelle
        result = arc.esd.manage_pasteObjects(cb_copy_data)
#        arc.esd.correctAllDocTypes()

        return arc   
        
    security.declareProtected("Modify portal content", "purge")
    def purge(self, REQUEST=None):
        """
        Deletes the content for this scenario but leaves the status unchanged.
        Documents are deleted if they are not part of any other scenario.
        If they are part of another scenario, only the tag for the current scenario is removed.
        """
        #TODO im EVENT auf Elandoc DB-Eintraege loeschen.
        m = self.content.Members
        mpath = "/".join(m.getPhysicalPath())
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        mdocs = self._getDocumentsForScenario(path=mpath)
        for doc in mdocs:
            self._purgeDocument(doc)
        g = self.content.Groups
        gpath = "/".join(g.getPhysicalPath())
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        gdocs = self._getDocumentsForScenario(path=gpath)
        for doc in gdocs:
            self._purgeDocument(doc)
        t = self.content.Transfers
        tpath = "/".join(t.getPhysicalPath())
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        tdocs = self._getDocumentsForScenario(path=tpath)
        for doc in tdocs:
            self._purgeDocument(doc)
        if REQUEST:
            portalMessage(self, _("There are no more documents for this scenario."), "info")
            return self.restrictedTraverse("view")()
        
    def _purgeDocument(self, source_brain):
        """
        Delete utility
        """
        source_obj = source_brain.getObject()
        # determine parent folder for copy
        scns = source_obj.scenarios
        if len(scns) == 1: # only the one scenario --> delete    
            p = parent(source_obj)
            p.manage_delObjects([source_obj.getId()])
        else: # Only remove the scenario
            scns = list(scns)
            scns.remove(self.getId())
            source_obj.scenarios=scns
            source_obj.reindexObject()
    
    def addScenarioForUsers(self):
        """
        Add this scenario to each users selection of scenarios.
        """
        pm = getToolByName(self, 'portal_membership')
        # TODO: nur für die eigenen Nutzer
        for memberId in pm.listMemberIds():
            member = pm.getMemberById(memberId)
            scns = list(member.getProperty("scenarios"))
            if self.getId() not in scns:
                scns.append(self.getId())
            member.setMemberProperties({"scenarios": scns})
    
    def deleteScenarioReferences(self):
        """
        """
        self.substitute = None
        self.reindexObject()
        
    def canBeAssigned(self):
        """
        Can this scenario be assigned to documents?
        Is it published? Is it active?
        """
        wftool = getToolByName(self, 'portal_workflow')
        return (wftool.getInfoFor(self, 'review_state') == 'published' and self.status == 'active')
##/code-section methods 


##code-section bottom

#@adapter(IELANContent, IObjectAddedEvent)
#def updateCreated(obj, event=None):
@adapter(IELANScenario, IObjectAddedEvent)
def scenarioAdded(obj, event=None):
    """
    For new scenarios, add them to each user's personal selection.
    """
    # print "scenarioAdded"
    obj.addScenarioForUsers()

@adapter(IELANScenario, IObjectModifiedEvent)
def scenarioChanged(obj, event=None):
    """
    """
    #print 'scenarioChanged'
    if obj.status != 'active':
        obj.deleteScenarioReferences()
    #print obj.substitute
    if obj.substitute:
        sscen = obj.substitute.to_object
        if not sscen.canBeAssigned():
            log("Substitute can not be assigned. Not published or not active.")
            return
        # Update all objects for this scenario
        m = obj.content
        mpath = "/".join(m.getPhysicalPath())
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        args = {'portal_type':'DPDocument', 'path': mpath}
        cat = getToolByName(obj, "portal_catalog")
        mdocs = cat(args) 
        for doc in mdocs:
            try:
                docobj = doc.getObject()
                scens = docobj.scenarios
                #print docobj, scens
                if scens and obj.getId() in scens:
                    scens.remove(obj.getId())
                    scens.append(sscen.getId())
                    docobj.scenarios = scens 
                    docobj.reindexObject()
                    #print "changed", docobj
            except Exception, e:
                log_exc(e)
                              
@adapter(IELANScenario, IActionSucceededEvent)
def scenarioPublished(obj, event=None):
    if event.__dict__['action'] == 'publish':        
        # Update all objects for this scenario
        m = obj.content
        mpath = "/".join(m.getPhysicalPath())
        args = {'portal_type':'DPDocument', 'path': mpath}
        cat = getToolByName(obj, "portal_catalog")
        mdocs = cat(args) 
        for doc in mdocs:
            try:
                docobj = doc.getObject()
                scens = docobj.scenarios
                #print docobj, scens
                if scens and obj.getId() in scens:
                    docobj.reindexObject()
                    #print "changed", docobj
            except Exception, e:
                log_exc(e)


##/code-section bottom 
