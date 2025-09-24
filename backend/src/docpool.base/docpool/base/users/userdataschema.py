from docpool.base import DocpoolMessageFactory as _
from docpool.base.interfaces import IDocpoolBaseLayer
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
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def current_dp_uid(context):
    if context.portal_type == "DocumentPool":
        return context.UID()


class IEnhancedUserDataSchema(model.Schema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """

    dp = schema.Choice(
        title=_("label_user_dp", default="DocPool"),
        description=_("description_user_dp", default=""),
        required=False,
        source="docpool.base.vocabularies.UserDocumentPools",
        defaultFactory=current_dp_uid,
    )


class EnhancedUserDataSchemaAdapter(AccountPanelSchemaAdapter):
    schema = IEnhancedUserDataSchema


@adapter(Interface, IDocpoolBaseLayer, UserDataPanel)
class UserDataPanelExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields["email"].field.required = False
        self.form.fields["dp"].field.readonly = False


@adapter(Interface, IDocpoolBaseLayer, RegistrationForm)
class RegistrationPanelExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields["email"].field.required = False


@adapter(Interface, IDocpoolBaseLayer, AddUserForm)
class AddUserFormExtender(extensible.FormExtender):
    def update(self):
        fields = field.Fields(IEnhancedUserDataSchema)
        self.add(fields)
        self.form.fields["email"].field.required = False
        if self.context.portal_type == "DocumentPool":
            self.form.fields["dp"].field.readonly = True
