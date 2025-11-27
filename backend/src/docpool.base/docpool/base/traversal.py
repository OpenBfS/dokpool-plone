from docpool.base.utils import get_current_appactive_markers
from zope.component import adapter
from zope.interface import alsoProvides
from ZPublisher.interfaces import IPubAfterTraversal


@adapter(IPubAfterTraversal)
def app_active_after_traversal_subscriber(event):
    for marker in get_current_appactive_markers():
        alsoProvides(event.request, marker)
