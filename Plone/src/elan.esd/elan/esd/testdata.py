# -*- coding: utf-8 -*-

import transaction
import time
from zExceptions import BadRequest
# from Acquisition import aq_base

# from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFPlone.utils import safe_unicode
from plone.app.textfield.value import RichTextValue
import datetime
from Products.CMFCore.utils import getToolByName
import random

from docpool.elan.config import ELAN_APP
from elan.policy.chomsky import chomsky
from loremipsum import get_paragraphs
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport

    

    
alldtypes = ['eventinformation',
           'notification',
           'nppinformation',
           'weatherinformation',
           'trajectory',
           'cncanprojection',
           'ifinprojection',
           'nppprojection',
           'rodosprojection',
           'otherprojection',
           'gammadoserate',
           'airactivity',
           'groundcontamination',
           'mresult_feed',
           'mresult_food',
           'mresult_water',
           'situationreport',
           'instructions',
           'protectiveactions',
           'mediarelease']

somedtypes = alldtypes[:8]

    
def deleteTestData(context):
    """
    """
    prefix = context.prefix or context.getId()
    gtool = getToolByName(context, 'portal_groups')
    gtool.removeGroups(['%s_Group1' % prefix, '%s_Group2' % prefix]) # also deletes the group folder via event subscribers
    mtool = getToolByName(context, 'portal_membership', None)
    mtool.deleteMembers(['%s_user1' % prefix, '%s_user2' % prefix]) # also deletes the member folders
    
    
def createTestDocuments(context, count):
    """
    """
    prefix = context.prefix or context.getId()
    count = int(count)
    for i in range(1, count):
        # random user
        u = int(round(random.random() + 1.0))
        uname = "%s_user%d" % (prefix, u)
        gname = "%s_Group%d" % (prefix, u)
        create_in_group = False
        if (int(round(random.random()))):
            create_in_group = True
        tn = int(random.random() * len(alldtypes))    
        etype = alldtypes[tn]
        
        path = None
        if create_in_group:
            path = context.content.Groups[gname]
        else:
            path = context.content.Members[uname.replace("-","--")]
        docid = "doc%d_%d" % (i, int(time.time()))
        # Generate random text for description
        
        d = chomsky(2)
        t = "<p>" + "</p><p>".join(get_paragraphs(3)) + "</p>"
        
        path.invokeFactory(id=docid, type_name="DPDocument", title="Document %d %s" % (i, uname), description=d)
        d = path._getOb(docid)
        d.docType = etype
        ILocalBehaviorSupport(d).local_behaviors = ['elan','transfers']
        d.text = RichTextValue(safe_unicode(t))
        s = int(round(random.random() + 1.0))
        if ELAN_APP in context.allSupportedApps():
            d.doc_extension(ELAN_APP).scenarios = ["scenario%d" % s]
        d.reindexObject()
    
def createGroupsAndUsers(context):    
    gtool = getToolByName(context, 'portal_groups')
    prefix = context.prefix or context.getId()
    prefix = str(prefix)
    title = context.Title()
    props = { 'allowedDocTypes' : alldtypes, 'title' : 'Group 1 (%s)' % title, 'description': 'Test Group 1', 'dp': context.UID() }
    gtool.addGroup("%s_Group1" % prefix, properties=props)
    props = { 'allowedDocTypes' : somedtypes, 'title' : 'Group 2 (%s)' % title, 'description': 'Test Group 2', 'dp': context.UID() }
    gtool.addGroup("%s_Group2" % prefix, properties=props)
    mtool = getToolByName(context, 'portal_membership', None)
    mtool.addMember('%s_user1' % prefix, 'User 1 (%s)' % title, ['Member'], [])
    user1 = mtool.getMemberById('%s_user1' % prefix) 
    user1.setMemberProperties(
            {"fullname": 'User 1 (%s)' % title,
             "dp": context.UID()})
    user1.setSecurityProfile(password="user1")
    mtool.createMemberArea('%s_user1' % prefix)
    gtool.addPrincipalToGroup('%s_user1' % prefix, '%s_Group1' % prefix)
    gtool.addPrincipalToGroup('%s_elanmanager' % prefix, '%s_Group1' % prefix)
    gtool.addPrincipalToGroup('%s_user1' % prefix, '%s_Members' % prefix)
    mtool.addMember('%s_user2' % prefix, 'User 2 (%s)' % title, ['Member'], [])
    user2 = mtool.getMemberById('%s_user2' % prefix)
    user2.setMemberProperties(
            {"fullname": 'User 2 (%s)' % title,
             "dp": context.UID()})
    user2.setSecurityProfile(password="user2")
    mtool.createMemberArea('%s_user2' % prefix)
    gtool.addPrincipalToGroup('%s_user2' % prefix, '%s_Group2' % prefix)
    gtool.addPrincipalToGroup('%s_user2' % prefix, '%s_Members' % prefix)
    transaction.commit()