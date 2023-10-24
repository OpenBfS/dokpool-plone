from docpool.base.marker import IImportingMarker
from docpool.rei.general.rei import install
from plone import api
from zope.globalrequest import getRequest


def post_install(context):
    if IImportingMarker.providedBy(getRequest()):
        return
    install(api.portal.get())
