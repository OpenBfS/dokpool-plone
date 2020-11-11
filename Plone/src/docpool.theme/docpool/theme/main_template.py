from Products.CMFPlone.browser.main_template import MainTemplate as OrigMainTemplate
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MainTemplate(OrigMainTemplate):

    popup_template = ViewPageTemplateFile('templates/popup_main_template.pt')

    def __call__(self):
        return self.template()

    @property
    def template(self):
        self.request.RESPONSE.setHeader('X-UA-Compatible', 'IE=edge,chrome=1')
        try:
            if (
                self.request.form.get('popup_load')
                or self.request['URL'].find('@@inline') > -1
            ):
                # Marked in the template as css class .bfs_popup
                return self.popup_template
            elif self.request.form.get('ajax_load'):
                return OrigMainTemplate.ajax_template
            else:
                return OrigMainTemplate.main_template
        except BaseException:
            return OrigMainTemplate.main_template
