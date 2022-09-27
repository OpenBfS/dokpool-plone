from plone import api


def post_install(context):
    # Add additional setup code here
    from docpool.config.general.elan import install

    install(api.portal.get())


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
