from docpool.base import DocpoolMessageFactory as _
from docpool.base.interfaces import IDocpoolBaseLayer
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.personalpreferences import PersonalPreferencesPanel
from plone.autoform import directives
from plone.supermodel import model
from plone.z3cform.fieldsets import extensible
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import adapter
from zope.interface import Interface


class IEnhancedPersonalPreferences(model.Schema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """

    apps = schema.List(
        title=_("label_user_apps", default="Applications"),
        description=_("description_user_apps", default=""),
        required=False,
        value_type=schema.Choice(source="docpool.base.vocabularies.AvailableApps"),
    )
    directives.widget(apps=CheckBoxFieldWidget)


class EnhancedPersonalPreferencesAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedPersonalPreferences

    def get_apps(self):
        return self.context.getProperty("apps", [])

    def set_apps(self, value):
        return self.context.setMemberProperties({"apps": value})

    dp = property(get_apps, set_apps)


@adapter(Interface, IDocpoolBaseLayer, PersonalPreferencesPanel)
class PersonalPreferencesPanelExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedPersonalPreferences)
        self.add(fields)
        # remove not needed fields
        self.remove("wysiwyg_editor")
        self.remove("language")
        self.remove("timezone")


# little monkey patch
def updateWidgets(self):
    super(PersonalPreferencesPanel, self).updateWidgets()
    # skip the other fields


PersonalPreferencesPanel.updateWidgets = updateWidgets
