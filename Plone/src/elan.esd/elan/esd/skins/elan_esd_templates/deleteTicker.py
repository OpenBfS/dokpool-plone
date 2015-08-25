## Script (Python) "deleteTicker.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Redirects to a default folder
##
if context.getId() == 'ticker':
    context.deleteText(context)
container.REQUEST.RESPONSE.redirect(context.absolute_url())
