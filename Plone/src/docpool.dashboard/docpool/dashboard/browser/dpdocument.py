#
# File: dpdocument.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from docpool.base.browser.flexible_view import FlexibleView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DPDocumentdashboardView(FlexibleView):
    """Additional View
    """

    __allow_access_to_unprotected_subobjects__ = 1
    __call__ = ViewPageTemplateFile('dpdocumentdashboard.pt')
