# -*- coding: utf-8 -*-
from Acquisition import aq_get
from Acquisition import aq_inner
from plone.app.discussion.browser.comments import CommentsViewlet
from plone.app.discussion.browser.conversation import ConversationView
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain
from zope.globalrequest import getRequest

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
        return True
    else:
        return self.original_enabled()


if not hasattr(ConversationView, "original_enabled"):
    ConversationView.original_enabled = ConversationView.enabled
    ConversationView.enabled = enabled


def is_archive(context):
    from docpool.base.content.dpdocument import IDPDocument
    return IDPDocument.providedBy(aq_inner(context)) and context.isArchive()


def is_discussion_allowed(self):
    return not is_archive(self.context) and self.original_is_discussion_allowed()


if not hasattr(CommentsViewlet, "original_is_discussion_allowed"):
    CommentsViewlet.original_is_discussion_allowed = (
        CommentsViewlet.is_discussion_allowed
    )
    CommentsViewlet.is_discussion_allowed = is_discussion_allowed


def edit_comment_allowed(self):
    return not is_archive(self.context) and self.original_edit_comment_allowed()


if not hasattr(CommentsViewlet, "original_edit_comment_allowed"):
    CommentsViewlet.original_edit_comment_allowed = (
        CommentsViewlet.edit_comment_allowed
    )
    CommentsViewlet.edit_comment_allowed = edit_comment_allowed


def can_edit(self, reply):
    return not is_archive(self.context) and self.original_can_edit(reply)


if not hasattr(CommentsViewlet, "original_can_edit"):
    CommentsViewlet.original_can_edit = CommentsViewlet.can_edit
    CommentsViewlet.can_edit = can_edit


def delete_own_comment_allowed(self):
    return not is_archive(self.context) and self.original_delete_own_comment_allowed()


if not hasattr(CommentsViewlet, "original_delete_own_comment_allowed"):
    CommentsViewlet.original_delete_own_comment_allowed = (
        CommentsViewlet.delete_own_comment_allowed
    )
    CommentsViewlet.delete_own_comment_allowed = delete_own_comment_allowed


def can_delete(self, reply):
    return not is_archive(self.context) and self.original_can_delete(reply)


if not hasattr(CommentsViewlet, "original_can_delete"):
    CommentsViewlet.original_can_delete = CommentsViewlet.can_delete
    CommentsViewlet.can_delete = can_delete


def getURL(self, relative=0, original=False):
    """
    Patched so we can provide special URLs for category documents in listings
    such as livesearch. The category objects are viewed within a collections (see @@dview)
    Also we make sure that sections don't get an URL, so they are not linked to in the navigation.
    """
    request = aq_get(self, 'REQUEST', None)
    if request is None:
        request = getRequest()
    if (
        # original set we ignore this special code
        (not original)
        # only valid for DPDocuments
        and self.portal_type == 'DPDocument'
        # resolveid does not exist in url
        and not request['URL'].find('resolveuid') > -1
        and not request['URL'].find('Transfers') > -1
        or 'overview' in str(request.get('myfolder_url',"/"))
    ):
        if self.cat_path:
            # This is it: we use the path of the category
            return "%s/@@dview?d=%s&disable_border=1" % (
                self.cat_path, self.UID)
        else:
            pass

    # This is the normal implementation
    return request.physicalPathToURL(self.getPath(), relative)

if not hasattr(AbstractCatalogBrain, "original_getURL"):
    AbstractCatalogBrain.original_getURL = AbstractCatalogBrain.getURL
    AbstractCatalogBrain.getURL = getURL


ssl._create_default_https_context = ssl._create_unverified_context
