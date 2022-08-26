from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DashboardView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("templates/dashboard.pt")
