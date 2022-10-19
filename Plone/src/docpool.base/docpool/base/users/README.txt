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
  * hide controlpanel-dropdown-navigation
Overrridden: UsersOverviewControlPanel.manageUser:
  * manageUser in order to change password reset behavior: set password == userid
    and to delete user folders - if possible - when user is deleted


Groups-Management
-----------------

Groups have two additional properties: allowedDocTypes, dp
These are initialized in docpool.config.general.base.createGroups when installing docpool.base
The available options are taken from the docpool.base.utils.possibleDocTypes and docpool.base.utils.possibleDocumentPools
To fix getting the option these are pachted onto GroupDataTool in docpool.base.monkey


view @@usergroup-groupdetails overridden for IPloneSiteRoot and IDocumentPool
Custom template usergroups_groupdetails.pt
  * links relative to docpool instead of portal
  * hide controlpanel-dropdown-navigation
  * hide links to Group Portlets and Group Dashboard
  * Only show if content is a DocumentPool
  * Allow value|title options in select and multiple select fields

TODO: Hide fields email, db from being editable when viewsing or adding a group (so far this is done in css):
https://redmine-koala.bfs.de/issues/2219
.portaltype-elanesd #formfield-form-esd, .portaltype-elanesd .field.esd, .template-user-information .field.portrait, .template-usergroup-groupdetails .field input[name="email:string"], .template-usergroup-groupdetails .field label[for="dp"], .template-usergroup-groupdetails .field label[for="email"], .template-usergroup-groupdetails .field select[name="dp:text"]

View GroupDetailsControlPanel subclassed:
  * set value of dp to content uuid (which is a DocumentPool)
  * when adding a group while inside a docpool title, descr and dp are set
  * Code unchanged since 5.0b1


View @@usergroup-groupmembership
Custom template usergroups_groupmembership.pt:
  * links relative to docpool instead of portal
  * hide controlpanel-dropdown-navigation
  * hide links to Group Portlets and Group Dashboard


View @@usergroup-groupprefs
Custom template usergroups_groupsoverview.pt:
  * links relative to docpool instead of portal
  * hide controlpanel-dropdown-navigation
