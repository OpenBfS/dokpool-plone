# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


PAS_TITLE = 'Trusted Proxy Auth'


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('docpool.policy_various.txt') is None:
        return
    portal = context.getSite()
    wtool = getToolByName(portal, 'portal_workflow')
    wtool.updateRoleMappings()
    cat = getToolByName(context.getSite(), "portal_catalog")
    #    cat.refreshCatalog(clear=True,pghandler=ZLogHandler(100))
    #    This would destroy the scenarios index
    setupTrustedProxyAuthPlugin(portal)


def _addPlugin(pas, pluginid='trusted_proxy_auth'):
    try:
        from pas.plugins.trustedproxyauth.plugin import TrustedProxyAuthPlugin
        from ZODB.PersistentList import PersistentList
    except:
        return PAS_TITLE + " product not installed"
    installed = pas.objectIds()
    if pluginid in installed:
        return PAS_TITLE + ' already installed.'
    plugin = TrustedProxyAuthPlugin(pluginid, title=PAS_TITLE)
    plugin.trusted_proxies = PersistentList(['127.0.0.1'])
    plugin.login_header = 'HTTP_X_REMOTE_USER'
    plugin.lowercase_logins = False
    plugin.lowercase_domain = False
    plugin.strip_nt_domain = True
    plugin.strip_ad_domain = True
    plugin.verify_login = False
    plugin.emulate_plone_login = True
    plugin.plone_login_timeout = 30

    pas._setObject(pluginid, plugin)
    plugin = pas[plugin.getId()]  # get plugin acquisition wrapped!
    for info in pas.plugins.listPluginTypeInfo():
        interface = info['interface']
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface, [x[0] for x in pas.plugins.listPlugins(interface)[:-1]]
        )


def setupTrustedProxyAuthPlugin(site):
    pas = site.acl_users
    _addPlugin(pas)
