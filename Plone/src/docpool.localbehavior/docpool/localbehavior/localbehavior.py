from Acquisition import aq_inner
from docpool.localbehavior import MessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import Interface, provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def initializeLocalBehaviors(context):
    dp_app_state = getMultiAdapter((context, getRequest()), name="dp_app_state")
    return list(dp_app_state.effectiveAppsHere())


@provider(IFormFieldProvider)
class ILocalBehaviorSupport(model.Schema):

    directives.widget(local_behaviors=CheckBoxFieldWidget)
    local_behaviors = schema.List(
        title="Behaviors",
        description=_(
            "description_local_behaviors",
            default="Select applications supported for this content,"
            " changes will be applied after saving",
        ),
        required=False,
        defaultFactory=initializeLocalBehaviors,
        value_type=schema.Choice(title="Applications", vocabulary="LocalBehaviors"),
    )


class ILocalBehaviorSupporting(Interface):
    """Marker"""


class LocalBehaviorSupport:
    def __init__(self, context):
        self.context = context

    def _get_local_behaviors(self):
        return list(set(self.context.local_behaviors))

    def _set_local_behaviors(self, value):
        if isinstance(value, type([])) or (isinstance(value, type(tuple))):
            value = list(set(value))
        context = aq_inner(self.context)
        if value is not None:
            context.local_behaviors = list(set(value))
        else:
            context.local_behaviors = []

    local_behaviors = property(_get_local_behaviors, _set_local_behaviors)
