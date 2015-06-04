# -*- coding: utf-8 -*-

from plone.directives.dexterity.form import EditForm, AddForm
from five.grok import context, name
from docpool.base.content.dpdocument import IDPDocument
from z3c.form import button
from docpool.base import ELAN_EMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.Archetypes.utils import shasattr

def checkUpload(form):
    context = form.getContent()
    if shasattr(context, "uploadsAllowed"):
        return context.uploadsAllowed() # we EDIT a document, that's simple 
    else:
        # We are CREATING a document, thus the object does not exist yet
        # context is the folder
        dp_type = context.REQUEST.get("form.widgets.docType")
        if dp_type:    
            try:
                dto = context.config[dp_type[0]]
                # print dto
                if dto.allowUploads:
                    return True
                else:
                    return False
            except:
                return False


class DPDocumentEditForm(EditForm):
    context(IDPDocument)
    
    @button.buttonAndHandler(_("label_continue", 
                               u'Continue with files & images'), 
                             name='continue',
                             condition=checkUpload)
    def handleContinue(self, action):
        EditForm.handleApply(self,action)
    
    @button.buttonAndHandler(PMF(u'Save'), name='save')
    def handleApply(self, action):
        EditForm.handleApply(self,action)
    
    @button.buttonAndHandler(PMF(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        EditForm.handleCancel(self, action)
        
        
class DPDocumentAddForm(AddForm):
    name('DPDocument')


    @button.buttonAndHandler(_("label_continue", 
                               u'Continue with files & images'), 
                             name='continue',
                             condition=checkUpload)
    def handleContinue(self, action):
        AddForm.handleAdd(self, action)
        
    @button.buttonAndHandler(PMF('Save'), name='save')
    def handleAdd(self, action):
        AddForm.handleAdd(self, action)

    @button.buttonAndHandler(PMF(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        AddForm.handleCancel(self, action)