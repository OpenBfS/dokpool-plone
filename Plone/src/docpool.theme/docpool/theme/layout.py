""" Override the default Plone layout utility.
"""
from docpool.base.content.dpdocument import IDPDocument
from plone import api
from plone.app.layout.globals import layout as base


class LayoutPolicy(base.LayoutPolicy):
    """
    Enhanced layout policy helper.

    Extend the Plone standard class to have some more <body> CSS classes
    based on the current context.
    """

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag.
        """

        # Get content parent
        body_class = base.LayoutPolicy.bodyClass(self, template, view)

        if IDPDocument.providedBy(self.context):
            state = api.content.get_state(obj=self.context)
            return body_class + " docstate-" + state
        else:
            return body_class
