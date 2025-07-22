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
    """Initialize local behaviors with the effective apps for the current context.
    
    This factory function is used as the default value provider for the local_behaviors
    field. It automatically sets the available applications based on what's currently
    effective in the DocumentPool context.
    
    Args:
        context: The content object context for which to determine effective apps
        
    Returns:
        list: List of application identifiers that are effective in this context
    """
    dp_app_state = getMultiAdapter((context, getRequest()), name="dp_app_state")
    return list(dp_app_state.effectiveAppsHere())


@provider(IFormFieldProvider)
class ILocalBehaviorSupport(model.Schema):
    """Schema interface for local behavior support.
    
    This interface provides the local_behaviors field that allows users to select
    which domain-specific applications (ELAN, REI, RODOS, DOKSYS) should be active
    for a specific DPDocument. This enables object-based behaviors rather than
    type-based behaviors, allowing different documents of the same type to have
    different functionality based on their assigned applications.
    
    The field is hidden for users without View management screens permission
    to prevent unauthorized modification of behavior assignments.
    """
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
    """Marker interface for content that supports local behaviors.
    
    Content types that implement this interface can have dynamic behaviors
    assigned on a per-object basis rather than per-type. This is the core
    mechanism that allows DPDocuments to have different functionality
    (input fields, views, workflows) based on which applications they
    are assigned to (ELAN, REI, RODOS, DOKSYS).
    """


@implementer(ILocalBehaviorSupport)
@adapter(IDexterityContent)
class LocalBehaviorSupport:
    """Adapter that provides local behavior support for Dexterity content.
    
    This adapter manages the local_behaviors attribute on content objects,
    ensuring that behavior assignments are stored and retrieved correctly.
    It handles deduplication and proper storage of the behavior list.
    
    The adapter is registered for all IDexterityContent objects but only
    becomes active when the content also provides ILocalBehaviorSupporting.
    """
    
    def __init__(self, context):
        """Initialize the adapter with the content context.
        
        Args:
            context: The Dexterity content object to adapt
        """
        self.context = context

    @property
    def local_behaviors(self):
        """Get the local behaviors assigned to this content object.
        
        Returns a deduplicated list of application identifiers that are
        currently assigned as local behaviors for this object.
        
        Returns:
            list: Unique list of application identifiers (e.g., ['elan', 'rei'])
        """
        lb = getattr(self.context.aq_base, "local_behaviors", [])
        return list(set(lb))

    @local_behaviors.setter
    def local_behaviors(self, value):
        """Set the local behaviors for this content object.
        
        Stores the provided application identifiers as local behaviors,
        ensuring deduplication and proper handling of None values.
        
        Args:
            value: List or tuple of application identifiers, or None
                  Examples: ['elan', 'rei'], ('doksys',), None
        """
        if isinstance(value, (list, tuple)):
            value = list(set(value))
        context = aq_inner(self.context)
        if value is not None:
            context.local_behaviors = list(set(value))
        else:
            context.local_behaviors = []
