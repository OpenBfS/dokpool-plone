# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter

from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName



from elan.irix import DocpoolMessageFactory as _

##code-section imports
##/code-section imports 

# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms. In this case, we don't
# have an edit form, since there are no editable options.

class Iirix_navigationPortlet(IPortletDataProvider):
##code-section interface
	pass
##/code-section interface

# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.

class Assignment(base.Assignment):
    implements(Iirix_navigationPortlet)

    ##code-section assignment
    ##/code-section assignment

    @property
    def title(self):
        return _(u"irix_navigation")

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).

class Renderer(base.Renderer):

    # render() will be called to render the portlet
    
    render = ViewPageTemplateFile('irix_navigation.pt')
       
    ##code-section renderer-methods    
    def objectstructure(self):
        """
        """
        return self.context.navigationHTML()
    ##/code-section renderer-methods
 
##code-section forms    
class AddForm(base.NullAddForm):
    
    # This method must be implemented to actually construct the object.

    def create(self):
        return Assignment()
##/code-section forms

##code-section bottom
##/code-section bottom