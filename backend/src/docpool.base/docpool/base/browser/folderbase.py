from AccessControl import Unauthorized
from Acquisition import aq_inner
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.folderbase import IFolderBase
from docpool.base.content.infolink import IInfoLink
from docpool.base.utils import extendOptions
from OFS.CopySupport import CopyError
from plone import api
from plone.app.content.browser.interfaces import IFolderContentsView
from plone.app.contenttypes.interfaces import ICollection
from plone.memoize import view
from Products.CMFCore.exceptions import ResourceLockedError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import transaction_note
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import field
from z3c.form import form
from ZODB.POSException import ConflictError
from zope.interface import implementer

import logging
import traceback
import transaction


log = logging.getLogger(__name__)


class FolderBaselistitemView(BrowserView):
    """Additional View"""

    __call__ = ViewPageTemplateFile("folderbaselistitem.pt")

    def options(self):
        return extendOptions(self.context, self.request, {})


class FolderBaserpopupView(BrowserView):
    """Additional View"""

    __call__ = ViewPageTemplateFile("folderbaserpopup.pt")


@implementer(IFolderContentsView)
class FolderBaseView(BrowserView):
    """Default view"""

    def dp_buttons(self, items):
        """
        Determine the available buttons by calling the original method from the
        folder_contents view.
        """
        return self.buttons(items)

    def buttons(self, items):
        buttons = []
        context = aq_inner(self.context)
        portal_actions = getToolByName(context, "portal_actions")
        button_actions = portal_actions.listActionInfos(
            object=context, categories=("folder_buttons",)
        )

        # Do not show buttons if there is no data, unless there is data to be
        # pasted
        if not len(items):
            if self.context.cb_dataValid():
                for button in button_actions:
                    if button["id"] == "paste":
                        return [self.setbuttonclass(button)]
            else:
                return []

        show_delete_action = False
        delete_action = [i for i in button_actions if i["id"] == "delete"]
        delete_action = delete_action[0] if delete_action else None
        if delete_action:
            for item in items:
                obj = item.getObject()
                if api.user.has_permission("Delete objects", obj=obj):
                    show_delete_action = True
                    # shortcut
                    break
        if not show_delete_action:
            button_actions.remove(delete_action)

        for button in button_actions:
            # Make proper classes for our buttons
            buttons.append(self.setbuttonclass(button))
        return buttons

    def setbuttonclass(self, button):
        if button["id"] == "paste":
            button["cssclass"] = "standalone"
        else:
            button["cssclass"] = "context"
        return button

    def getFolderContents(self, kwargs):
        """ """
        contentlisting = self.context.restrictedTraverse("@@contentlisting")
        kwargs["object_provides"] = [
            IFolderBase.__identifier__,
            ICollection.__identifier__,
        ]
        res = [b for b in contentlisting(**kwargs)]
        apps = self.isFilteredBy()
        if apps:
            kwargs["apps_supported"] = apps[0]
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


class FolderAction:
    def view_url(self):
        context_state = api.content.get_view(
            "plone_context_state", self.context, self.request
        )
        return context_state.view_url()

    def redirect(self):
        return self.request.response.redirect(self.view_url())

    def redirect_info(self, msg):
        api.portal.show_message(msg, self.request)
        self.redirect()

    def redirect_error(self, msg):
        api.portal.show_message(msg, self.request, "error")
        self.redirect()


class FolderDeleteForm(form.Form, FolderAction):
    """Delete multiple items by path
    Modernized version of folder_delete.cpy (of Plone 4).
    Called from a folder or collection with actions using a folder_button with string:@@folder_delete:method
    Partly stolen from plone.app.content.browser.actions.DeleteConfirmationForm
    """

    fields = field.Fields()
    template = ViewPageTemplateFile("templates/delete_confirmation.pt")
    enableCSRFProtection = True

    def more_info(self):
        """Render linkintegrity-info for all items that are to be deleted."""
        portal = api.portal.get()
        paths = self.request.get("paths", [])
        # We use unrestrictedTraverse because the user may not have access to all parents
        objects = [portal.unrestrictedTraverse(path) for path in paths]
        objects = [i for i in objects if self.check_delete_permission(i)]
        if not objects:
            return self.redirect_info(_("No items to delete."))
        adapter = api.content.get_view(
            "delete_confirmation_info", self.context, self.request
        )
        if adapter:
            return adapter(objects)
        return ""

    @button.buttonAndHandler(_("Delete"), name="Delete")
    def handle_delete(self, action):
        paths = self.request.get("paths", [])
        objects = [api.content.get(path=str(path)) for path in paths]
        objects = [i for i in objects if self.check_delete_permission(i)]
        if objects:
            # linkintegrity was already checked and maybe ignored!
            api.content.delete(objects=objects, check_linkintegrity=False)
            return self.redirect_info(_("Items deleted."))
        else:
            return self.redirect_info(_("No items deleted."))

    @button.buttonAndHandler(_("label_cancel", default="Cancel"), name="Cancel")
    def handle_cancel(self, action):
        return self.redirect()

    def updateActions(self):
        super().updateActions()
        if self.actions and "Delete" in self.actions:
            self.actions["Delete"].addClass("btn-danger")
        if self.actions and "Cancel" in self.actions:
            self.actions["Cancel"].addClass("btn-secondary")

    def check_delete_permission(self, obj):
        return api.user.has_permission("Delete objects", obj=obj)


class FolderCutForm(BrowserView, FolderAction):
    def __call__(self):
        if not (paths := self.request.get("paths", [])):
            return self.redirect_error(_("Please select one or more items to cut."))

        ids = [p.removesuffix("/").rpartition("/")[-1] for p in paths]
        try:
            self.context.manage_cutObjects(ids, self.request)
        except CopyError:
            msg = _("One or more items not moveable.")
        except AttributeError:
            msg = _("One or more selected items is no longer available.")
        except ResourceLockedError:
            msg = _("One or more selected items is locked.")
        else:
            transaction_note(f"Cut {ids} from {self.context.absolute_url()}")
            return self.redirect_info(
                _("${count} item(s) cut.", mapping={"count": len(ids)})
            )

        return self.redirect_error(msg)


class FolderPasteForm(BrowserView, FolderAction):
    def __call__(self):
        if not self.context.cb_dataValid:
            transaction.abort()
            return self.redirect_error(_("Copy or cut one or more items to paste."))

        if "__cp" not in self.request:
            transaction.abort()
            return self.redirect__error(_("Paste could not find clipboard content."))

        try:
            self.context.manage_pasteObjects(self.request["__cp"])
        except ConflictError:
            raise
        except ValueError:
            msg = _("Disallowed to paste item(s).")
        except Unauthorized:
            msg = _("Unauthorized to paste item(s).")
        except Exception as e:
            if isinstance(e, CopyError) and "Item Not Found" in str(e):
                msg = _(
                    "The item you are trying to paste could not be found. "
                    "It may have been moved or deleted after you copied or cut it. "
                )
            else:
                msg = _("Unknown error occured. Please check your logs")
                log.exception("Exception during pasting")
                log.exception(traceback.format_exception(e))
        else:
            transaction_note("Pasted content to %s" % (self.context.absolute_url()))
            return self.redirect_info(_("Item(s) pasted."))

        transaction.abort()
        return self.redirect_error(msg)
