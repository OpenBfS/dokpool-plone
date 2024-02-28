from plone import api
from plone.app.z3cform.views import BootstrapActions
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from zope.interface import classImplements


class AddForm(BootstrapActions, add.DefaultAddForm):
    def updateWidgets(self):
        """"""
        super().updateWidgets()
        # see https://redmine-koala.bfs.de/issues/5432
        # This is a fix for setting local_behaviors for users who may chose them.
        # When local_behaviors is skipped the defaultFactory will no be used to set a default value.
        # Setting the field to hidden will still use the defaultFactory.
        if "ILocalBehaviorSupport.local_behaviors" not in self.widgets:
            return
        if not api.user.has_permission("zope2.ViewManagementScreens", obj=self.context):
            self.widgets["ILocalBehaviorSupport.local_behaviors"].mode = "hidden"


class AddView(add.DefaultAddView):
    form = AddForm


class EditForm(BootstrapActions, edit.DefaultEditForm):
    def updateWidgets(self):
        super().updateWidgets()
        # See https://redmine-koala.bfs.de/issues/5432
        # Hide local_behaviors
        if "ILocalBehaviorSupport.local_behaviors" not in self.widgets:
            return
        if not api.user.has_permission("zope2.ViewManagementScreens", obj=self.context):
            self.widgets["ILocalBehaviorSupport.local_behaviors"].mode = "hidden"


EditView = layout.wrap_form(EditForm)
classImplements(EditView, IDexterityEditForm)
