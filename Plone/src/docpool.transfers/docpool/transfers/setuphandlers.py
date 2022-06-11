from plone import api


def post_install(setup=None):
    from docpool.config.general.transfers import install

    install(api.portal.get())
