# -*- coding: utf-8 -*-
from docpool.users import DocpoolMessageFactory as _
from docpool.users.interfaces import IDocPoolUsersLayer
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.register import AddUserForm
from plone.app.users.browser.register import RegistrationForm
from plone.app.users.browser.userdatapanel import UserDataPanel
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from zope import schema
from zope.component import adapts
from zope.interface import Interface


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
