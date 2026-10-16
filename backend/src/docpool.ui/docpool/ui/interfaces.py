from plone.app.z3cform.interfaces import IPloneFormLayer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


# Needs to be more specific than the old theme for jbot overrides to win.
class IUITheme(IDefaultBrowserLayer, IPloneFormLayer):
    """Marker interface that defines a Zope 3 browser layer."""
