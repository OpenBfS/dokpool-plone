from plone.app.textfield.value import RichTextValue
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides


class DeleteTicker(BrowserView):
    def __call__(self):
        if self.context.id == "ticker":
            alsoProvides(self.request, IDisableCSRFProtection)
            self.context.text = RichTextValue("", "text/plain", "text/html")
        self.request.response.redirect(self.context.absolute_url())
