# -*- coding: utf-8 -*-
#
# File: folderbase.py
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
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.folderbase import IFolderBase
from docpool.base.content.infolink import IInfoLink
from docpool.base.utils import extendOptions
from plone import api
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.contenttypes.interfaces import ICollection
from plone.memoize import view
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope.interface import implementer


class FolderBaselistitemView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('folderbaselistitem.pt')

    def options(self):
        return extendOptions(self.context, self.request, {})


class FolderBaserpopupView(BrowserView):
    """Additional View
    """

    __call__ = ViewPageTemplateFile('folderbaserpopup.pt')


@implementer(IFolderContentsView)
class FolderBaseView(BrowserView):
    """Default view
    """

    def dp_buttons(self, items):
        """
        Determine the available buttons by calling the original method from the
        folder_contents view.
        """
        return self.buttons(items)

    def buttons(self, items):
        context = aq_inner(self.context)
        portal_actions = getToolByName(context, 'portal_actions')
        button_actions = portal_actions.listActionInfos(
            object=context, categories=('folder_buttons',)
        )
        actions_by_id = {action['id']: action for action in button_actions}

        # Do not show buttons if there is no data, unless there is data to be
        # pasted
        if not items:
            if 'paste' in actions_by_id and self.context.cb_dataValid():
                return [self.setbuttonclass(actions_by_id['paste'])]
            else:
                return []

        if 'delete' in actions_by_id and not any(
            api.user.has_permission('Delete objects', obj=item.getObject())
            for item in items
        ):
            button_actions.remove(actions_by_id['delete'])

        # Make proper classes for our buttons
        buttons = [self.setbuttonclass(action) for action in button_actions]
        return buttons

    def setbuttonclass(self, button):
        if button['id'] == 'paste':
            button['cssclass'] = 'standalone'
        else:
            button['cssclass'] = 'context'
        return button

    def getFolderContents(self, kwargs):
        """
        """
        contentlisting = self.context.restrictedTraverse('@@contentlisting')
        kwargs["object_provides"] = [
            IFolderBase.__identifier__,
            ICollection.__identifier__,
        ]
        res = [b for b in contentlisting(**kwargs)]
        apps = self.isFilteredBy()
        if apps:
            kwargs['apps_supported'] = apps[0]
        kwargs["object_provides"] = [
            IDPDocument.__identifier__,
            IInfoLink.__identifier__,
        ]
        res.extend([b for b in contentlisting(**kwargs)])
        return res

    @view.memoize
    def isFilteredBy(self):
        """

        @return:
        """
        user = api.user.get_current()
        res = user.getProperty("filter_active") or False
        if res:
            res = user.getProperty("apps") or []
        # print "filter_active ", res
        return res


class FolderDeleteForm(form.Form):
    """Delete multiple items by path
    Modernized version of folder_delete.cpy (of Plone 4).
    Called from a folder or collection with actions using a folder_button with string:@@folder_delete:method
    Partly stolen from plone.app.content.browser.actions.DeleteConfirmationForm
    """

    fields = field.Fields()
    template = ViewPageTemplateFile('templates/delete_confirmation.pt')
    enableCSRFProtection = True

    def view_url(self):
        context_state = api.content.get_view('plone_context_state', self.context, self.request)
        return context_state.view_url()

    def more_info(self):
        """Render linkintegrity-info for all items that are to be deleted."""
        paths = self.request.get('paths', [])
        objects = [api.content.get(path=str(path)) for path in paths]
        objects = [i for i in objects if self.check_delete_permission(i)]
        if not objects:
            api.portal.show_message(_(u'No items to delete.'), self.request)
            return self.request.response.redirect(self.view_url())
        adapter = api.content.get_view('delete_confirmation_info', self.context, self.request)
        if adapter:
            return adapter(objects)
        return ""

    @button.buttonAndHandler(_('Delete'), name='Delete')
    def handle_delete(self, action):
        paths = self.request.get('paths', [])
        objects = [api.content.get(path=str(path)) for path in paths]
        objects = [i for i in objects if self.check_delete_permission(i)]
        if objects:
            # linkintegrity was already checked and maybe ignored!
            api.content.delete(objects=objects, check_linkintegrity=False)
            api.portal.show_message(_(u'Items deleted.'), self.request)
        else:
            api.portal.show_message(_(u'No items deleted.'), self.request)
        target = self.view_url()
        return self.request.response.redirect(target)

    @button.buttonAndHandler(
        _('label_cancel', default='Cancel'), name='Cancel')
    def handle_cancel(self, action):
        target = self.view_url()
        return self.request.response.redirect(target)

    def updateActions(self):
        super(FolderDeleteForm, self).updateActions()
        if self.actions and 'Delete' in self.actions:
            self.actions['Delete'].addClass('btn-danger')
        if self.actions and 'Cancel' in self.actions:
            self.actions['Cancel'].addClass('btn-secondary')

    def check_delete_permission(self, obj):
        return api.user.has_permission('Delete objects', obj=obj)
