# -*- coding: UTF-8 -*-
"""A BrowserView to replace the Controller Python Script "folder_publish"
"""
from DateTime import DateTime
from plone import api
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from docpool.base import DocpoolMessageFactory as _
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ZODB.POSException import ConflictError
from zope.i18n import translate
from zope.interface import implementer


class WorkflowActionView(BrowserView):

    template = ViewPageTemplateFile('templates/dpdocument_transition_form.pt')

    def __call__(self):
        form = self.request.form
        self.pworkflow = getToolByName(self.context, 'portal_workflow')
        self.putils = getToolByName(self.context, 'plone_utils')
        self.transition_id = form.get('transition', None)
        self.comments = form.get('comments', '')
        self.recurse = form.get('recurse', 'no') == 'yes'
        self.transitions = []
        self.items = []
        self.errors = []
        # the folder_listing passes paths
        paths = self.request.get('paths', [])
        for path in paths:
            obj = api.content.get(path=path)
            if not obj:
                continue
            item = {
                'title': obj.title,
                'path': path,
                'obj': obj,
                'transitions': [],
            }
            for transition in self.pworkflow.getTransitionsFor(obj):
                transition_title = translate(transition['name'], domain='plone', context=self.request)
                tdata = {
                    'id': transition['id'],
                    'title': transition_title
                }
                item['transitions'].append(transition_title)
                if tdata not in self.transitions:
                    self.transitions.append(tdata)
            if item['transitions']:
                self.items.append(item)

        if not form.get('form.button.submit'):
            return self.template()

        # transition items
        transitioned = 0
        for item in self.items:
            obj = item['obj']
            if self.transition(obj):
                transitioned += 1

        if self.errors:
            return self.template()
        else:
            msg = _('${transitioned} Items transitioned!', mapping={'transitioned': transitioned})
            api.portal.show_message(msg, self.request)
            return self.request.response.redirect(self.context.absolute_url())

    def transition(self, obj, bypass_recurse=False):
        transitions = self.pworkflow.getTransitionsFor(obj)
        if self.transition_id in [t['id'] for t in transitions]:
            try:
                # set effective date if not already set
                if obj.EffectiveDate() == 'None':
                    obj.setEffectiveDate(DateTime())

                self.pworkflow.doActionFor(obj, self.transition_id,
                                           comment=self.comments)
                if self.putils.isDefaultPage(obj):
                    self.transition(obj.aq_parent, bypass_recurse=True)
                recurse = self.recurse and not bypass_recurse
                if recurse and IFolderish.providedBy(obj):
                    for sub in obj.values():
                        self.transition(sub)
                obj.reindexObject()
                return True
            except ConflictError:
                raise
            except Exception:
                self.errors.append(
                    _('Could not transition: ${title}',
                      mapping={'title': obj.title}))
