from plone import api
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.schema.interfaces import IVocabularyFactory

import logging


log = logging.getLogger(__name__)


def add_user(
    docpool,
    username,
    groupnames=None,
    enabled_apps=["elan", "doksys", "rei"],
):
    """Create a User and a Group for a docpool for testing.

    This mimicks adding groups in the application in docpool.users by:
    * adding the docpool-prefix to the groups id and title
    * allowing all doctypes
    * assigning the docpool

    """
    docpool_title = docpool.Title()
    prefix = docpool.prefix or docpool.id
    docpool_uid = IUUID(docpool)
    groupnames = groupnames if groupnames else []
    for groupname in groupnames:
        add_group(docpool, groupname)

    password = username
    password = f"dp_{username}"
    # add the user
    user_fullname = f"{username} ({docpool_title})"
    user = api.user.create(
        email="tester@plone.org",
        username=username,
        password=password,
        roles=("Member",),
        properties={"fullname": user_fullname},
    )
    user.setMemberProperties(
        {
            "fullname": user_fullname,
            "dp": docpool_uid,
            "apps": enabled_apps,
        }
    )
    # add the user to specified groups
    for groupname in groupnames:
        real_groupname = f"{prefix}_{groupname}"
        group = api.group.get(real_groupname)
        api.group.add_user(group=group, user=user)

    # Add the user to app-specific default-groups
    api.group.add_user(groupname=f"{prefix}_Members", user=user)
    if "doksys" in enabled_apps:
        api.group.add_user(groupname=f"{prefix}_DoksysUsers", user=user)
    if "elan" in enabled_apps:
        api.group.add_user(groupname=f"{prefix}_ELANUsers", user=user)
    if "rei" in enabled_apps:
        api.group.add_user(groupname=f"{prefix}_REIUsers", user=user)
    pm = getToolByName(docpool, "portal_membership")
    pm.createMemberArea(username)
    return user


def add_group(docpool, groupname):
    """Add a group in a docpool.

    This mimicks adding groups in the application by:
    * adding the docpool-prefix to the groups id and title
    * put all doctypes in memberdata to allow creating all DPDocuments
    * put docpool-id in memberdata
    """
    # get all doctypes to enable them for the new group
    voc = getUtility(IVocabularyFactory, name="docpool.base.vocabularies.DocType")
    doctypes = voc(docpool, raw=True)
    doctypes_ids = [i[0] for i in doctypes]
    # Do not create reireports. Can be added after creating the group.
    if "reireport" in doctypes_ids:
        doctypes_ids.remove("reireport")

    gtool = getToolByName(docpool, "portal_groups")
    docpool_uid = IUUID(docpool)
    docpool_title = docpool.Title()
    group_title = f"{groupname.capitalize()} ({docpool_title})"
    description = ""
    prefix = docpool.prefix or docpool.id
    groupname = f"{prefix}_{groupname}"

    if api.group.get(groupname=groupname) is not None:
        log.info(f"Skipping. Group {groupname} exists.")
        return

    props = {
        "title": group_title,
        "description": description,
        "dp": docpool_uid,
        "allowedDocTypes": doctypes_ids,
    }
    request = getRequest()
    if request.method != "POST":
        # fool addGroup to allow to work even without a real POST
        request.method = "POST"
    # this uses the monkey-patched addGroup from docpool.users
    # it will create a group-folder inside the docpool
    gtool.addGroup(
        id=groupname,
        roles=(),
        groups=(),
        properties=props,
        REQUEST=request,
        title=group_title,
        description=description,
    )
    return api.group.get(groupname)
