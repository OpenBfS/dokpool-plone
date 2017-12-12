## Python Script "logoutjs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

return """   <script type='text/javascript'>
   function close_overview() {
        chron=window.open('','Overview','');chron.close();
        window.location.href= '%s/logout';
    }   
   </script>""" % context.portal_url()
