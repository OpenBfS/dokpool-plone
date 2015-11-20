from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFPlone.browser.main_template import MainTemplate as OrigMainTemplate


class MainTemplate(OrigMainTemplate):

    popup_template = ViewPageTemplateFile('templates/popup_main_template.pt')

    def __call__(self):
        return self.template()

    @property
    def template(self):
        if self.request.form.get('popup_load') or self.request['URL'].find('@@inline') > - 1:
            return self.popup_template
        elif self.request.form.get('ajax_load'):
            return OrigMainTemplate.ajax_template
        else:
            return OrigMainTemplate.main_template
