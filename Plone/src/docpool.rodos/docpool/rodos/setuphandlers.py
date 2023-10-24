from docpool.base.marker import IImportingMarker
from plone import api
from zope.globalrequest import getRequest


def post_install(setup=None):
    if IImportingMarker.providedBy(getRequest()):
        return
    from docpool.rodos.general.rodos import install

    install(api.portal.get())
