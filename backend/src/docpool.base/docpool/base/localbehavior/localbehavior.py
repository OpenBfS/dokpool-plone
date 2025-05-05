from Acquisition import aq_inner
from docpool.base import DocpoolMessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def initializeLocalBehaviors(context):
    dp_app_state = getMultiAdapter((context, getRequest()), name="dp_app_state")
    return list(dp_app_state.effectiveAppsHere())


@provider(IFormFieldProvider)
class ILocalBehaviorSupport(model.Schema):
    # Note: This field is set to hidden in add and edit forms
    # for users without View management screens (zope2.ViewManagementScreens)
    # See https://redmine-koala.bfs.de/issues/5432
    directives.widget(local_behaviors=CheckBoxFieldWidget)
    local_behaviors = schema.List(
        title="Behaviors",
        description=_(
            "description_local_behaviors",
            default="Select applications supported for this content, changes will be applied after saving",
        ),
        required=False,
        defaultFactory=initializeLocalBehaviors,
        missing_value=[],
        value_type=schema.Choice(title="Applications", vocabulary="LocalBehaviors"),
    )


class ILocalBehaviorSupporting(Interface):
    """Marker"""


@implementer(ILocalBehaviorSupport)
@adapter(IDexterityContent)
class LocalBehaviorSupport:
    def __init__(self, context):
        self.context = context

    @property
    def local_behaviors(self):
        lb = getattr(self.context.aq_base, "local_behaviors", [])
        return list(set(lb))

    @local_behaviors.setter
    def local_behaviors(self, value):
        if isinstance(value, (list, tuple)):
            value = list(set(value))
        context = aq_inner(self.context)
        if value is not None:
            context.local_behaviors = list(set(value))
        else:
            context.local_behaviors = []
