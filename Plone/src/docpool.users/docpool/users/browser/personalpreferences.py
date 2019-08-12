# -*- coding: utf-8 -*-
from plone.app.users.browser.personalpreferences import PersonalPreferencesPanel
from zope.interface import Interface, implements
from zope import schema
from plone.app.users.schema import checkEmailAddress
from Products.CMFPlone import PloneMessageFactory as _p
from docpool.users import DocpoolMessageFactory as _
from plone.supermodel import model

from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.register import RegistrationForm, AddUserForm
from plone.z3cform.fieldsets import extensible
from zope.component import adapts
from docpool.users.interfaces import IDocPoolUsersLayer
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.directives import form


class IEnhancedPersonalPreferences(model.Schema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """

    apps = schema.List(
        title=_(u'label_user_apps', default=u'Applications'),
        description=_(u'description_user_apps', default=u''),
        required=False,
        value_type=schema.Choice(source="docpool.base.vocabularies.AvailableApps"),
    )
    form.widget(apps=CheckBoxFieldWidget)


class EnhancedPersonalPreferencesAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedPersonalPreferences

    def get_apps(self):
        return self.context.getProperty('apps', [])

    def set_apps(self, value):
        return self.context.setMemberProperties({'apps': value})

    dp = property(get_apps, set_apps)


class PersonalPreferencesPanelExtender(extensible.FormExtender):
    adapts(Interface, IDocPoolUsersLayer, PersonalPreferencesPanel)

    def update(self):
        fields = field.Fields(IEnhancedPersonalPreferences)
        self.add(fields)
        # remove not needed fields
        self.remove('wysiwyg_editor')
        self.remove('language')
        self.remove('timezone')


# little monkey patch
def updateWidgets(self):
    super(PersonalPreferencesPanel, self).updateWidgets()
    # skip the other fields


PersonalPreferencesPanel.updateWidgets = updateWidgets
