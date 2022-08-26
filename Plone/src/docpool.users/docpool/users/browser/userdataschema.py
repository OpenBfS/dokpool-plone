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
from zope.component import adapter
from zope.interface import Interface


class IEnhancedUserDataSchema(model.Schema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """

    dp = schema.Choice(
        title=_("label_user_dp", default="DocPool"),
        description=_("description_user_dp", default=""),
        required=False,
        source="docpool.base.vocabularies.UserDocumentPools",
    )


class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema

    def get_dp(self):
        return self.context.getProperty("dp", "")

    def set_dp(self, value):
        return self.context.setMemberProperties({"dp": value})

    dp = property(get_dp, set_dp)


@adapter(Interface, IDocPoolUsersLayer, UserDataPanel)
class UserDataPanelExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields["email"].field.required = False


@adapter(Interface, IDocPoolUsersLayer, RegistrationForm)
class RegistrationPanelExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields["email"].field.required = False


@adapter(Interface, IDocPoolUsersLayer, AddUserForm)
class AddUserFormExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields["email"].field.required = False
