from docpool.rei.general.rei import install
from plone import api


def post_install(context):
    install(api.portal.get())
