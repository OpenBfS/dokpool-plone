from plone import api


def post_install(setup=None):
    from docpool.rodos.general.rodos import install

    install(api.portal.get())
