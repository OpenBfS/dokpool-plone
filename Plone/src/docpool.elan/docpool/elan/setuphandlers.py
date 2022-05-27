# -*- coding: utf-8 -*-
from plone import api


def post_install(context):
    # Add additional setup code here
    from docpool.config.general.elan import install
    install(api.portal.get())
