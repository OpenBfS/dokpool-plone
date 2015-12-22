import random
from docpool.base.utils import getGroupsForCurrentUser
try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
from zope.component import getUtility
from zope.interface import implements

from wsapi4plone.core.browser.interfaces import IApplicationAPI
from wsapi4plone.core.browser.wsapi import WSAPI
from wsapi4plone.core.interfaces import IScrubber, IService, IServiceContainer
from plone import api
from Products.CMFCore.utils import getToolByName
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

class ApplicationAPI(WSAPI):
    implements(IApplicationAPI)

    def _get_object_data(self, obj):
        if obj:       
            serviced_obj = IService(obj)
            data = serviced_obj.get_object()
            type_ = serviced_obj.get_type()
            misc = serviced_obj.get_misc()
            return (self.builder.get_path(obj, ''), (data, type_, misc,))
        else:
            return ()
        
    
    def get_primary_documentpool(self):
        """
        Return the ESD the user belongs to - or the first one he has access to if he is a global user.
        """
        site = self.context
        esd = site.myPersonalDocumentPool()
        return self._get_object_data(esd)

    def get_plone_object(self, basepath, objpath=None):
        """
        """
        if objpath:
            opath = "%s/%s" % (basepath, objpath)
        else:
            opath = basepath
        obj = self.builder(self.context, opath)
        return self._get_object_data(obj)

    def get_user_folder(self, esdpath):
        """
        Return the user folder object within the ESD under esdpath.
        Will produce an error if the user does not belong to that ESD.
        """
        user = api.user.get_current()
        username = user.getUserName().replace("-", "--")
        ufpath = "content/Members/%s" % username
        return self.get_plone_object(esdpath, ufpath)
        
    def get_group_folders(self, esdpath):
        user = api.user.get_current()
        esd = self.context.restrictedTraverse(esdpath)
        groups = getGroupsForCurrentUser(esd, user)
        if not groups: # User is reader only
            return {}
        ids = []
        for group in groups:
            if group['etypes']: # Group is ELAN group which can produce documents
                ids.append(group['id'])
        
        q = { 'path': esdpath + "/content/Groups", 'portal_type': "GroupFolder", 'getId': ids }
        return self.context.restrictedTraverse("@@query")(q) 
    
    def get_transfer_folders(self, esdpath):
        q = { 'path': esdpath + "/content/Transfers", 'portal_type': "ELANTransferFolder" }
        return self.context.restrictedTraverse("@@query")(q) 
    
    def create_dp_document(self, folderpath, id, title, description, text, docType, scenario):
        """
        Creates a document under folderpath.
        """
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        
        params = { str(folderpath) + "/" + str(id)  : [ { "title": title, 
                                   "description" : description,
                                   "text" : text,
                                   "docType" : docType,
                                   "scenarios" : [scenario]} , "DPDocument"] }
        # Delegate to post_object
        res = self.context.restrictedTraverse("@@post_object")(params)
        return res[0] # just the path
    
    def upload_file(self, path, id, title, description, data, filename):
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        
        print "upload_file"
        params = { str(path) + "/" + str(id) : [ { "title": title, 
                                   "description" : description,
                                   "file" : (data, filename)} , "File"] }
        # Delegate to post_object
        print params
        res = self.context.restrictedTraverse("@@post_object")(params)
        return res[0] # just the path
        
    def upload_image(self, path, id, title, description, data, filename):
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        print "upload_image"
        
        params = { str(path) + "/" + str(id)  : [ { "title": title, 
                                   "description" : description,
                                   "image" : (data, filename)} , "Image"] }
        print params
        # Delegate to post_object
        res = self.context.restrictedTraverse("@@post_object")(params)
        return res[0] # just the path
        
    def autocreate_subdocuments(self, path):
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        # Delegate to post_object
        doc = self.context.restrictedTraverse(path)
        return doc.autocreateSubdocuments() # just the path

    def read_properties_from_file(self, path):
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        # Delegate to post_object
        doc = self.context.restrictedTraverse(path)
        return doc.readPropertiesFromFile() # just the path

    def post_user(self, username, password, fullname, esdpath):
        """
        """
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        
        properties = {"fullname":fullname}
        esd = api.content.get(esdpath, None)
        if esd:
            properties['dp'] = esd.UID()
            properties['fullname'] = "{} ({})".format(fullname, esd.Title()) 
        mtool = getToolByName(esd, 'portal_membership', None)    
        mtool.addMember(username, password, ['Member'], [])
        user = mtool.getMemberById(username) 
        user.setMemberProperties(properties)
        user.setSecurityProfile(password=password)
#Nur mit email-Adresse        
#         user = api.user.create(email=email, 
#                                username=username,
#                                password=password,
#                                roles=['Member'],
#                                properties=properties)
        mtool.createMemberArea(username)
        return user.getMemberId()
    
    def post_group(self, groupname, title, description, esdpath):
        """
        """
        


        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        
        esd = api.content.get(esdpath, None)
        prefix = esd.prefix
        prefix = str(prefix)
        groupprops = {'title': title,
                      'description': description}
        if esd:
            groupprops['dp'] = esd.UID()
            title += " ({})".format(esd.Title())
            groupprops['title'] = title
#        group = api.group.create(groupname=groupname, title=title, description=description, roles=[], groups=[])
        gtool = getToolByName(self, 'portal_groups')
        group = gtool.addGroup("%s_%s" % (prefix, groupname),
                   properties=groupprops)

#        if groupprops:
#            group.setGroupProperties(groupprops)
        if group:
             return  groupname
        else:
             return "fail"
    
    def put_group(self, groupname, title, description, esdpath, allowedDocTypes):
        """
        """
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        
        props = { 'allowedDocTypes' : allowedDocTypes,
                  'title' : title,
                  'description': description}
        esd = api.content.get(esdpath, None)
        if esd:
            title = "{} ({})".format(props['title'], esd.Title())
            props['dp'] = esd.UID()
            props['title'] = title
        group = api.group.get(groupname)
        message = "notChanged"
        if group:
            group.setProperties(props)
            gTitle = group.getProperty('title') == title
            gDescription = group.getProperty('description') == description
            gEsd = group.getProperty('dp') == esd.UID()
            gAllowedDocTypes = group.getProperty('allowedDocTypes') == allowedDocTypes
            if gTitle and gDescription and gEsd and gAllowedDocTypes:
                message = "changed" 
        return message
        
    def add_user_to_group(self, username, groupname, esdpath):
        """
        """
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        
        esd = api.content.get(esdpath, None)
        prefix = esd.prefix
        prefix = str(prefix)

        groupname = prefix + "_" + groupname
        api.group.add_user(groupname=groupname, group=None, username=username, user=None)
        group = api.group.get(groupname)
        message = "notAdded"
        if group:
            if username in group.getAllGroupMemberIds():
                message = "added"
        return message
        
        
        

