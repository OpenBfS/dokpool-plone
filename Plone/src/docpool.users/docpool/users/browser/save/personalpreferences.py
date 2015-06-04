from Acquisition import aq_inner
from AccessControl import Unauthorized

from zope.component import getUtility
from zope.component import adapts
from zope.formlib.interfaces import WidgetInputError
from zope.formlib.itemswidgets import DropdownWidget
from zope.interface import implements, Interface
from zope import schema
from zope.schema import ValidationError
from zope.schema import Choice
from zope.schema import Bool
from zope.formlib import form

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from plone.app.users.browser.account import AccountPanelForm
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.userdataschema import IUserDataSchemaProvider

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFDefault.formlib.widgets import FileUploadWidget
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import set_own_login_name, safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.users.browser.personalpreferences import PasswordPanelAdapter as PPA,\
    IPasswordSchema, UserDataPanel
from docpool.base.content.documentpool import IDocumentPool








class UserDataConfiglet(UserDataPanel):
    """ """
    template = ViewPageTemplateFile('account-configlet.pt')



class PasswordPanelAdapter(PPA):

    adapts(IDocumentPool)
    implements(IPasswordSchema)



