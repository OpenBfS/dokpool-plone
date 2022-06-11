import logging
import ssl
import traceback

from Acquisition import aq_get, aq_inner
from plone.app.discussion.browser.conversation import ConversationView
from Products.PlonePAS.tools.memberdata import MemberData
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain
from zope.globalrequest import getRequest

log = logging.getLogger(__name__)


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
        if not context.restrictedTraverse("@@context_helpers").is_archive():
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
    Patched so we can provide special URLs for category documents in listings
    such as livesearch. The category objects are viewed within a collections (see @@dview)
    Also we make sure that sections don't get an URL, so they are not linked to in the navigation.
    """
    request = aq_get(self, "REQUEST", None)
    if request is None:
        request = getRequest()
    if (
        # original set we ignore this special code
        (not original)
        # only valid for DPDocuments
        and self.portal_type == "DPDocument"
        # resolveid does not exist in url
        and not request["URL"].find("resolveuid") > -1
        and not request["URL"].find("Transfers") > -1
        or "overview" in str(request.get("myfolder_url", "/"))
    ):
        if self.cat_path:
            # This is it: we use the path of the category
            return f"{self.cat_path}/@@dview?d={self.UID}&disable_border=1"
        else:
            pass

    # This is the normal implementation
    return request.physicalPathToURL(self.getPath(), relative)


if not hasattr(AbstractCatalogBrain, "original_getURL"):
    AbstractCatalogBrain.original_getURL = AbstractCatalogBrain.getURL
    AbstractCatalogBrain.getURL = getURL


ssl._create_default_https_context = ssl._create_unverified_context


def setMemberProperties(self, mapping, **kw):
    # We're never interested in login times as sessions are created by SSO anyway.
    # Login times used to be the main cause by far for writing member properties, which
    # are suspected to be a DB hotspot causing ConflictErrors, see #4325.
    for key in ("login_time", "last_login_time"):
        mapping.pop(key, None)
    if not mapping:
        return

    # XXX 4325: temporarily keep watching the member property setter to confirm that
    # removal of login time logging actually prevents most DB ConflictErrors.
    request = aq_get(self, "REQUEST", None)
    if request is None:
        request = getRequest()
    log.info(
        "Setting member properties:\n{} at {}\n{}".format(
            str(list(mapping)),
            request["URL"],
            "\n".join(item.splitlines()[0] for item in traceback.format_stack()),
        )
    )
    self._orig_setMemberProperties(mapping, **kw)


MemberData._orig_setMemberProperties = MemberData.setMemberProperties
MemberData.setMemberProperties = setMemberProperties
