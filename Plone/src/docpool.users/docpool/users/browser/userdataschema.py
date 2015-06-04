# -*- coding: utf-8 -*-
from zope.interface import Interface, implements
from zope import schema
from plone.app.users.schema import checkEmailAddress
from Products.CMFPlone import PloneMessageFactory as _p
from docpool.users import ELAN_EMessageFactory as _
from Products.CMFDefault.formlib.schema import FileUpload
from plone.supermodel import model

from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.app.users.browser.register import RegistrationForm, AddUserForm
from plone.z3cform.fieldsets import extensible
from zope.component import adapts
from docpool.users.interfaces import IDocPoolUsersLayer
from z3c.form import field

class IEnhancedUserDataSchema(model.Schema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """

    dp = schema.Choice(
                        title=_(u'label_user_dp', default=u'DocPool'),
                        description=_(u'description_user_dp', default=u''),
                        required=False,
                        source="docpool.base.vocabularies.UserDocumentPools",
                        )

class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema

    def get_dp(self):
        return self.context.getProperty('dp', '')
    def set_dp(self, value):
        return self.context.setMemberProperties({'dp': value})
    dp = property(get_dp, set_dp)


class UserDataPanelExtender(extensible.FormExtender):
    adapts(Interface, IDocPoolUsersLayer, UserDataPanel)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields['email'].field.required = False

class RegistrationPanelExtender(extensible.FormExtender):
    adapts(Interface, IDocPoolUsersLayer, RegistrationForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields['email'].field.required = False

class AddUserFormExtender(extensible.FormExtender):
    adapts(Interface, IDocPoolUsersLayer, AddUserForm)

    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields['email'].field.required = False