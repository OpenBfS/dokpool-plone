from plone import api
from Products.CMFCore.utils import getToolByName
from zope.globalrequest import getRequest


def post_install(context):
    portal = api.portal.get()
    from docpool.config.general.base import install

    install(portal)
    cat = getToolByName(portal, "portal_catalog")
    cat.reindexIndex(["dp_type", "mdate", "changed"], REQUEST=getRequest())

    # A Folder called "Members" is needed to create userfolders before they are moved
    # to the content-area
    if "Members" not in portal:
        members = api.content.create(
            container=portal,
            type="Folder",
            id="Members",
            title="Members",
            exclude_from_nav=True,
        )
        members.setLayout("@@member-search")

    # Show debug commit hash
    api.portal.set_registry_record("docpool.show_debug_info", True)
