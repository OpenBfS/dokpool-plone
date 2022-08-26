from plone import api


PAS_TITLE = "Trusted Proxy Auth"


def post_install(context):
    """Post install script"""
    wtool = api.portal.get_tool("portal_workflow")
    wtool.updateRoleMappings()
    setupTrustedProxyAuthPlugin()


def _addPlugin(pas, pluginid="trusted_proxy_auth"):
    try:
        from pas.plugins.trustedproxyauth.plugin import TrustedProxyAuthPlugin
        from ZODB.PersistentList import PersistentList
    except BaseException:
        return PAS_TITLE + " product not installed"
    installed = pas.objectIds()
    if pluginid in installed:
        return PAS_TITLE + " already installed."
    plugin = TrustedProxyAuthPlugin(pluginid, title=PAS_TITLE)
    plugin.trusted_proxies = PersistentList(["127.0.0.1"])
    plugin.login_header = "HTTP_X_REMOTE_USER"
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
        interface = info["interface"]
        if not interface.providedBy(plugin):
            continue
        pas.plugins.activatePlugin(interface, plugin.getId())
        pas.plugins.movePluginsDown(
            interface, [x[0] for x in pas.plugins.listPlugins(interface)[:-1]]
        )


def setupTrustedProxyAuthPlugin():
    pas = api.portal.get_tool("acl_users")
    _addPlugin(pas)


def uninstall(context):
    """Uninstall script"""
