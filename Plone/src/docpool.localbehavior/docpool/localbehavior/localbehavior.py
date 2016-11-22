from zope.component import getMultiAdapter
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from docpool.localbehavior import MessageFactory as _
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from Acquisition import aq_inner
from zope.interface import Interface

class ILocalBehaviorSupport(form.Schema):

    form.widget(local_behaviors=CheckBoxFieldWidget)
    local_behaviors = schema.List(
        title=u'Behaviors',
        description=_(u'description_local_behaviors', default=u'Select applications supported for this content,' +
                     ' changes will be applied after saving'),
        required=False,
        value_type=schema.Choice(
            title=u'Applications',
            vocabulary="LocalBehaviors"
        )
    )

alsoProvides(ILocalBehaviorSupport,IFormFieldProvider)

@form.default_value(field=ILocalBehaviorSupport['local_behaviors'])
def initializeLocalBehaviors(data):
    self = data.context
    dp_app_state = getMultiAdapter((self, self.REQUEST), name=u'dp_app_state')
    return dp_app_state.effectiveAppsHere()


class ILocalBehaviorSupporting(Interface):
    """Marker"""


class LocalBehaviorSupport(object):
    def __init__(self, context):
        self.context = context

    def _get_local_behaviors(self):
        return self.context.local_behaviors

    def _set_local_behaviors(self, value):
        #print "setLocalBehaviors", value
        context = aq_inner(self.context)
        context.local_behaviors = value

    local_behaviors = property(_get_local_behaviors, _set_local_behaviors)

