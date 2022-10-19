Changes to users and groups management for docpool
==================================================

The base of old customisations was maybe Plone 5.0b1 (early 2015)


view @@user-information overridden only for IDocumentPool
only changes are in template account-configlet.pt:
  * links relative to docpool instead of portal
  * hide user-preferences
  * hide controlpanel-dropdown-navigation (TODO)
registered in docpool.base.users.userdatapanel.UserDataConfiglet


view @@usergroup-usermembership overridden only for IDocumentPool
only changes are in template usergroups_usermembership.pt:
  * links relative to docpool instead of portal
  * hide user-preferences
  * hide controlpanel-dropdown-navigation
registered in docpool.base.users.userdatapanel.UserDataConfiglet


view @@usergroup-userprefs overridden only for IDocumentPool
Custom template usergroups_usersoverview.pt:
  * links relative to docpool instead of portal
  * hide user-preferences
  * hide controlpanel-dropdown-navigation
Overrridden: UsersOverviewControlPanel.manageUser:
  * manageUser in order to change password reset behavior: set password == userid
    and to delete user folders - if possible - when user is deleted
