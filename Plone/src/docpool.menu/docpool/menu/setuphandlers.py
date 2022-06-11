def post_install(context):
    """Post install script"""
    if context.readDataFile('docpoolmenu_default.txt') is None:
        return
    # Do something during the installation of this package


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile('docpoolmenu_uninstall.txt') is None:
        return
    # Do something during the uninstallation of this package
