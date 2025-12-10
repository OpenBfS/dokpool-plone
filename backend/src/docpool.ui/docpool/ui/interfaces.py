from docpool.theme.interfaces import ICustomTheme
from plone.app.z3cform.interfaces import IPloneFormLayer


# Needs to be more specific than the old theme for jbot overrides to win.
class IUITheme(ICustomTheme, IPloneFormLayer):
    """Marker interface that defines a Zope 3 browser layer."""
