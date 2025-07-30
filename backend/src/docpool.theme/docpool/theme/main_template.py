from plone import api
from Products.CMFPlone.browser.main_template import MainTemplate as OrigMainTemplate
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MainTemplate(OrigMainTemplate):
    # popup_main_template.pt is a file in this package, the default templates are in CMFPlone
    # We need to hack all cases where the local template is actually initialilzed

    popup_template_name = "templates/popup_main_template.pt"

    @property
    def template_name(self):
        if self.request.form.get("popup_load") or self.request["URL"].find("@@inline") > -1:
            return self.popup_template_name
        return super().template_name

    def __call__(self):
        if self.template_name == self.popup_template_name:
            return ViewPageTemplateFile(self.popup_template_name)
        self.request.response.setHeader(
            "X-Debug-User", "anonymous" if api.user.is_anonymous() else api.user.get_current().id
        )
        return super().__call__()

    @property
    def macros(self):
        return self.__call__().macros
