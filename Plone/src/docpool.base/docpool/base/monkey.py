# -*- coding: utf-8 -*-
from Acquisition import aq_get
from Acquisition import aq_inner
from plone.app.discussion.browser.conversation import ConversationView
from Products.ZCatalog.CatalogBrains import _GLOBALREQUEST_INSTALLED
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain
from Products.ZCatalog.CatalogBrains import getRequest

import ssl


# from plone.app.controlpanel.usergroups import UsersOverviewControlPanel


# Patches for the automatic creation of group folders


def enabled(self):
    """
    Needs to be patched, so that comments are enabled for the DPDocument type.
    Normally, they cannot be enabled for a folderish type.
    """
    # print "enabled"
    from docpool.base.content.dpdocument import IDPDocument

    context = aq_inner(self.context)
    if IDPDocument.providedBy(context):
        if not context.isArchive():
            return True
        else:
            return False
    else:
        return self.original_enabled()


if not hasattr(ConversationView, "original_enabled"):
    ConversationView.original_enabled = ConversationView.enabled
    ConversationView.enabled = enabled


def getURL(self, relative=0, original=False):
    """
    Patched so we can provide special URLs for documents in listings such as livesearch.
    Also we make sure that sections don't get an URL, so they are not linked to in the navigation.
    """
    request = aq_get(self, 'REQUEST', None)
    if request is None and _GLOBALREQUEST_INSTALLED:
        request = getRequest()
    if (
        (not original)
        and self.portal_type == 'DPDocument'
        and not request['URL'].find('resolveuid') > -1
        and not request['URL'].find('/content/') > -1
    ):
        if self.cat_path:
            # This is it: we use the path of the category
            return "%s/@@dview?d=%s&disable_border=1" % (
                self.cat_path, self.UID)
        else:
            pass
            # print "no cat_path"

    # This is the normal implementation
    return request.physicalPathToURL(self.getPath(), relative)


if not hasattr(AbstractCatalogBrain, "original_getURL"):
    AbstractCatalogBrain.original_getURL = AbstractCatalogBrain.getURL
    AbstractCatalogBrain.getURL = getURL


ssl._create_default_https_context = ssl._create_unverified_context
