# -*- coding: utf-8 -*-
from docpool.rei import DocpoolMessageFactory as _
from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.rei.config import REI_APP
from plone import api
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations

import logging

log = logging.getLogger(__name__)


def dpAdded(docpool):
    """
    @param docpool: a new docpool
    @return:

    """
    annotations = IAnnotations(docpool)
    fresh = REI_APP not in annotations[APPLICATIONS_KEY]
    if fresh:
        annotations[APPLICATIONS_KEY].append(REI_APP)

    if fresh:
        # connectTypesAndCategories(docpool) # TOOD: only when REI doctypes need to be added to ELAN categories
        # docpool.rei.correctAllDocTypes() # TODO: if the run display templates contains collections
        # with references to global doctypes, which need to be adapted to local
        # doctypes.
        copyberichte(docpool)
        createREIUsers(docpool)
        createREIGroups(docpool)
    log.info(u'Rebuilding catalog...')
    docpool.reindexAll()

    # TODO: further initializations?


def copyberichte(docpool):
    """

    @param docpool: a docpool
    @param fresh:
    @return:
    """
    portal = api.portal.get()
    berichte = portal['berichte']
    from docpool.base.utils import _copyPaste

    _copyPaste(berichte, docpool, safe=False)
    docpool.berichte.setTitle(_("Berichte"))
    docpool.berichte.local_behaviors=['rei']
    docpool.berichte.reindexObject()
    # make sure the folder berichte is first
    # TODO if more complex (e.g. second after 'esd')
    docpool.moveObject("berichte", 0)


def dpRemoved(docpool):
    """
    @param docpool: a docpool
    @return:
    """
    # TODO:
    return


def createREIGroups(docpool):
    """
    Create Group for rei application access
    @param self:
    @return:
    """

    prefix = docpool.prefix or docpool.getId()
    prefix = str(prefix)
    title = docpool.Title()
    gtool = getToolByName(docpool, 'portal_groups')
    # Group for REI application rights
    props = {
        'allowedDocTypes': [],
        'title': 'REI Users (%s)' % title,
        'description': 'Users with access to REI functions.',
        'dp': docpool.UID(),
    }
    gtool.addGroup("%s_REIUsers" % prefix, properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_REIUsers' % prefix)

    # Group for REI content administration - if needed, otherwise ignore...
    props = {
        'allowedDocTypes': [],
        'title': 'REI Content Administrators (%s)' % title,
        'description': 'Responsible for the definition of structure and types.',
        'dp': docpool.UID(),
    }
    gtool.addGroup("%s_REIContentAdministrators" % prefix, properties=props)
    gtool.addPrincipalToGroup(
        '%s_dpadmin' % prefix, '%s_REIContentAdministrators' % prefix
    )
    gtool.addPrincipalToGroup(
        '%s_reiadmin' %
        prefix,
        '%s_Administrators' %
        prefix)

    # Set REI role as a local role for the new group
    docpool.manage_setLocalRoles("%s_REIUsers" % prefix, ["REIUser"])
    # Set content admin access to config
    docpool.config.manage_setLocalRoles(
        "%s_REIContentAdministrators" % prefix, ["Owner"]
    )
    # and to navigation
    docpool.berichte.manage_setLocalRoles(
        "%s_REIContentAdministrators" % prefix, ["ContentAdmin"]
    )


def createREIUsers(docpool):
    # Set type for user folders
    mtool = getToolByName(docpool, "portal_membership")
    prefix = docpool.prefix or docpool.getId()
    prefix = str(prefix)
    title = docpool.Title()
    mtool.addMember(
        '%s_reiadmin' % prefix, 'REI Administrator (%s)' % title, [
            'Member'], []
    )
    reiadmin = mtool.getMemberById('%s_reiadmin' % prefix)
    reiadmin.setMemberProperties(
        {"fullname": 'REI Administrator (%s)' % title, "dp": docpool.UID()}
    )
    reiadmin.setSecurityProfile(password="admin")
