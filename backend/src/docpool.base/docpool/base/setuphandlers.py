from plone import api
from Products.CMFCore.utils import getToolByName
from Products.Sessions import install_session_data_manager
from Products.Transience.Transience import TransientObjectContainer
from Products.ZODBMountPoint.MountedObject import manage_addMounts
from zope.globalrequest import getRequest


def post_install(context):
    portal = api.portal.get()
    create_session_stuff(portal)
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


def create_session_stuff(portal):
    if api.env.test_mode():
        return
    app = portal.__parent__
    if "temp_folder" in app:
        return
    manage_addMounts(app, ["/temp_folder"])
    temp_folder = app.temp_folder
    default_sdc_settings = {
        "addNotification": "",
        "delNotification": "",
        "limit": 1000,
        "period_secs": 20,
        "timeout_mins": 20,
        "title": "Session Data Container",
    }
    sdc = TransientObjectContainer("session_data", **default_sdc_settings)
    temp_folder._setObject("session_data", sdc)
    install_session_data_manager(app)
