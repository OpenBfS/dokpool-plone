from StringIO import StringIO
from DateTime import DateTime
from plone.subrequest import subrequest
from urllib import unquote

from xhtml2pdf.pisa import pisaDocument
from xhtml2pdf import pisa
from PyPDF2 import PdfFileWriter, PdfFileReader

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
import logging


class PrintView(BrowserView):
    def _generatePDF(self, raw=False):
        """
        """

        def fetch_resources(uri, rel):
            """
            Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
            `uri` is the href attribute from the html link element.
            `rel` gives a relative path, but it's not used here.
            """
            urltool = getToolByName(self.context, "portal_url")
            portal = urltool.getPortalObject()
            base = portal.absolute_url()
            if uri.startswith(base):
                response = subrequest(unquote(uri[len(base) + 1 :]))
                if response.status != 200:
                    return None
                try:
                    # stupid pisa doesn't let me send charset.
                    ctype, encoding = response.getHeader('content-type').split(
                        'charset='
                    )
                    ctype = ctype.split(';')[0]
                    # pisa only likes ascii css
                    data = (
                        response.getBody()
                        .decode(encoding)
                        .encode('ascii', errors='ignore')
                    )

                except ValueError:
                    ctype = response.getHeader('content-type').split(';')[0]
                    data = response.getBody()

                data = data.encode("base64").replace("\n", "")
                data_uri = 'data:{0};base64,{1}'.format(ctype, data)
                return data_uri
            return uri

        pisa.showLogging(debug=True)
        #         REQUEST = self.REQUEST

        # open output file for writing (truncated binary)
        # resultFile = os.tmpfile() #open(outputFilename, "w+b")
        resultFile = StringIO()
        html = self.context.restrictedTraverse('@@print')()

        # convert HTML to PDF
        pisaStatus = pisa.CreatePDF(
            html,  # the HTML to convert
            dest=resultFile,
            debug=True,
            link_callback=fetch_resources,
        )  # file handle to recieve result

        # print pisaStatus.err

        resultFile.seek(0)
        pdfcontent = resultFile.read()

        # close output file
        resultFile.close()  # close output file
        now = DateTime()
        nice_filename = '%s_%s' % (self.context.getId(), now.strftime('%Y%m%d'))

        if not raw:
            self.request.response.setHeader(
                "Content-Disposition", "attachment; filename=%s.pdf" % nice_filename
            )
            self.request.response.setHeader("Content-Type", "application/pdf")
            self.request.response.setHeader("Content-Length", len(pdfcontent))
            self.request.response.setHeader(
                'Last-Modified', DateTime.rfc822(DateTime())
            )
            self.request.response.setHeader("Cache-Control", "no-store")
            self.request.response.setHeader("Pragma", "no-cache")
            self.request.response.write(pdfcontent)
        return pdfcontent

    def __call__(self):
        return self._generatePDF()
