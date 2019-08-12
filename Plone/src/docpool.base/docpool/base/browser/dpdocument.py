# -*- coding: utf-8 -*-
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


from Acquisition import aq_inner
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.dpdocument import IDPDocument
from plone import api
from plone.app.content.browser.file import FileUploadView as BaseFileUploadView
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.app.layout.globals.interfaces import IViewView
from plone.protect.interfaces import IDisableCSRFProtection
from plone.uuid.interfaces import IUUID
from Products.Archetypes.utils import contentDispositionHeader
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import alsoProvides
from zope.interface import implements

import json
import mimetypes
import urllib


class DPDocumentView(FlexibleView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('dpdocument.pt')

    def base_url(self):
        """
        """
        context = aq_inner(self.context)
        return context.restrictedTraverse('@@plone').getCurrentFolderUrl()

    def quote_plus(self, string):
        """
        """
        return urllib.quote_plus(string)

    def getFolderContents(self, kwargs):
        """
        """
        kwargs["object_provides"] = [IDPDocument.__identifier__]
        res = [b for b in self.context.getFolderContents(kwargs)]
        return res

    def dp_buttons(self, items):
        return []


class DPDocumentlistitemView(FlexibleView):
    """Additional View
    """

    __allow_access_to_unprotected_subobjects__ = 1
    __call__ = ViewPageTemplateFile('dpdocumentlistitem.pt')

    def ctype_short(self, file):
        """
        """
        # print file
        ctype = str(file.file.contentType)
        s = ctype.split('/')
        if len(s) == 2:
            return s[1]
        else:
            return s[0]


class DPDocumentinlineView(DPDocumentView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('dpdocumentinline.pt')
    implements(IViewView)


class DPDocumentprintView(FlexibleView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('dpdocumentprint.pt')
    implements(IViewView)


class DPDocumentdocimageView(BrowserView):
    """Additional View
    """

    def __call__(self):
        """
        This is the image - if possible without the legend
        """
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)
        refresh = request.get("refresh", False)
        response = request.RESPONSE
        response.setHeader('Content-Type', 'image/png')
        response.setHeader('Cache-control', 'max-age=300,s-maxage=300,must-revalidate')

        # Get doc image but without legend
        data, filename = self.context.getMyImage(refresh=refresh, full=False)

        header_value = contentDispositionHeader(
            'inline', filename=filename, charset='latin-1'
        )
        response.setHeader('Content-disposition', header_value)
        response.setHeader('Content-Length', len(data))
        return data


class FileUploadView(BaseFileUploadView):
    """Redirect to the workspace view so we can inject."""

    def __call__(self):
        result = self.process_request()
        if self.request.get_header('HTTP_ACCEPT') == 'application/json':
            self.request.response.setHeader("Content-type", "application/json")
            return json.dumps(result)
        else:
            self.request.response.redirect(self.context.absolute_url())

    def process_request(self):
        # XXX: We don't support the TUS resumable file upload protocol.
        # The pat-upload pattern supports it (due to mockup) and
        # plone.app.content.browser.file.py also supports it, but at the cost
        # of not being able to upload multiple files at once. We decided that
        # that's more important at the moment.
        if self.request.REQUEST_METHOD != 'POST':
            return []
        result = []
        form = self.request.form
        for name in [k for k in form.keys() if k.startswith('file')]:
            output = self.create_file_from_request(name)
            if output:
                result.append(output)
        return result

    def create_file_from_request(self, name):
        context = self.context
        filedata = self.request.form.get(name, None)
        if not filedata:
            return
        filename = filedata.filename
        content_type = mimetypes.guess_type(filename)[0] or ""
        # Determine if the default file/image types are DX or AT based
        ctr = api.portal.get_tool('content_type_registry')
        type_ = ctr.findTypeName(filename.lower(), '', '') or 'File'
        pt = api.portal.get_tool('portal_types')

        obj = IDXFileFactory(context)(filename, content_type, filedata)
        if hasattr(obj, 'file'):
            size = obj.file.getSize()
            content_type = obj.file.contentType
        elif hasattr(obj, 'image'):
            size = obj.image.getSize()
            content_type = obj.image.contentType
        else:
            return
        result = {"type": content_type, "size": size}
        result.update(
            {
                'url': obj.absolute_url(),
                'name': obj.getId(),
                'UID': IUUID(obj),
                'filename': filename,
            }
        )
        return result
