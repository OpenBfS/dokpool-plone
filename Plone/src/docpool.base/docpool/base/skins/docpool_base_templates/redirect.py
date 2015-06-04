## Script (Python) "redirect.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Redirects to a default folder
##
if context.isAdmin():
    container.REQUEST.RESPONSE.redirect(context.portal_url() + "/esd")
else:
    container.REQUEST.RESPONSE.redirect(context.myFirstDocumentPool())
