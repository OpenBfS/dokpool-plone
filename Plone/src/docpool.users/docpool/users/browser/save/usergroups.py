import logging
from smtplib import SMTPException

from AccessControl import getSecurityManager
from Acquisition import aq_inner
from zExceptions import Forbidden
from itertools import chain

from zope.interface import Interface
from zope.component import adapts, getAdapter, getMultiAdapter, getUtility
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.schema import Bool
from ZTUtils import make_query

from plone.protect import CheckAuthenticator
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.statusmessages.interfaces import IStatusMessage
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin

from plone.app.controlpanel.form import ControlPanelForm, ControlPanelView
#from plone.app.controlpanel.security import ISecuritySchema
#from plone.app.controlpanel.usergroups import UsersOverviewControlPanel as UOCP, \
#    GroupsOverviewControlPanel as GOCP, \
#    UsersGroupsControlPanelView as UGCPV
from plone.app.controlpanel.security import SecurityControlPanelAdapter as SCPA

logger = logging.getLogger('plone.app.controlpanel')

class IUserGroupsSettingsSchema(Interface):

    many_groups = Bool(title=_(u'Many groups?'),
                       description=_(u"Determines if your Plone is optimized "
                           "for small or large sites. In environments with a "
                           "lot of groups it can be very slow or impossible "
                           "to build a list all groups. This option tunes the "
                           "user interface and behaviour of Plone for this "
                           "case by allowing you to search for groups instead "
                           "of listing all of them."),
                       default=False)

    many_users = Bool(title=_(u'Many users?'),
                      description=_(u"Determines if your Plone is optimized "
                          "for small or large sites. In environments with a "
                          "lot of users it can be very slow or impossible to "
                          "build a list all users. This option tunes the user "
                          "interface and behaviour of Plone for this case by "
                          "allowing you to search for users instead of "
                          "listing all of them."),
                      default=False)

class UserGroupsSettingsControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IUserGroupsSettingsSchema)

    def __init__(self, context):
        super(UserGroupsSettingsControlPanelAdapter, self).__init__(context)
        pprop = getToolByName(context, 'portal_properties')
        self.context = pprop.site_properties

    many_groups = ProxyFieldProperty(IUserGroupsSettingsSchema['many_groups'])
    many_users = ProxyFieldProperty(IUserGroupsSettingsSchema['many_users'])

class UserGroupsSettingsControlPanel(ControlPanelForm):

    base_template = ControlPanelForm.template
    template = ZopeTwoPageTemplateFile('usergroupssettings.pt')

    form_fields = FormFields(IUserGroupsSettingsSchema)

    label = _("User/Groups settings")
    description = _("User and groups settings for this site.")
    form_name = _("User/Groups settings")

class SecurityControlPanelAdapter(SCPA):
    pass

class UsersGroupsControlPanelView(UGCPV):

    def membershipSearch(self, searchString='', searchUsers=True, searchGroups=True, ignore=None):
        """Search for users and/or groups, returning actual member and group items
           Replaces the now-deprecated prefs_user_groups_search.py script"""
        if ignore is None:
            ignore = []
        groupResults = userResults = []

        gtool = getToolByName(self, 'portal_groups')
        mtool = getToolByName(self, 'portal_membership')

        searchView = getMultiAdapter((aq_inner(self.context), self.request), name='pas_search')

        if searchGroups:
            groupResults = searchView.merge(chain(*[searchView.searchGroups(**{field: searchString}) for field in ['id', 'title']]), 'groupid')
            groupResults = [gtool.getGroupById(g['id']) for g in groupResults if g['id'] not in ignore]
            groupResults = [ g for g in groupResults if g.getProperty("dp") == self.context.UID()]
            groupResults.sort(key=lambda x: x is not None and normalizeString(x.getGroupTitleOrName()))

        if searchUsers:
            userResults = searchView.merge(chain(*[searchView.searchUsers(**{field: searchString}) for field in ['name', 'fullname', 'email']]), 'userid')
            userResults = [mtool.getMemberById(u['id']) for u in userResults if u['id'] not in ignore]
            userResults = [ u for u in userResults if u.getProperty("dp") == self.context.UID()]
            userResults.sort(key=lambda x: x is not None and x.getProperty('fullname') is not None and normalizeString(x.getProperty('fullname')) or '')

        return groupResults + userResults


class UsersOverviewControlPanel(UOCP):

    def doSearch(self, searchString):
        acl = getToolByName(self, 'acl_users')
        rolemakers = acl.plugins.listPlugins(IRolesPlugin)

        mtool = getToolByName(self, 'portal_membership')

        searchView = getMultiAdapter((aq_inner(self.context), self.request), name='pas_search')

        # First, search for all inherited roles assigned to each group.
        # We push this in the request so that IRoles plugins are told provide
        # the roles inherited from the groups to which the principal belongs.
        self.request.set('__ignore_group_roles__', False)
        self.request.set('__ignore_direct_roles__', True)
        inheritance_enabled_users = searchView.merge(chain(*[searchView.searchUsers(**{field: searchString}) for field in ['name', 'fullname', 'email']]), 'userid')
        allInheritedRoles = {}
        for user_info in inheritance_enabled_users:
            userId = user_info['id']
            user = acl.getUserById(userId)
            # play safe, though this should never happen
            if user is None:
                logger.warn('Skipped user without principal object: %s' % userId)
                continue
            allAssignedRoles = []
            for rolemaker_id, rolemaker in rolemakers:
                # getRolesForPrincipal can return None
                roles = rolemaker.getRolesForPrincipal(user) or ()
                allAssignedRoles.extend(roles)
            allInheritedRoles[userId] = allAssignedRoles

        # We push this in the request such IRoles plugins don't provide
        # the roles from the groups the principal belongs.
        self.request.set('__ignore_group_roles__', True)
        self.request.set('__ignore_direct_roles__', False)
        explicit_users = searchView.merge(chain(*[searchView.searchUsers(**{field: searchString}) for field in ['login', 'fullname', 'email']]), 'userid')

        # Tack on some extra data, including whether each role is explicitly
        # assigned ('explicit'), inherited ('inherited'), or not assigned at all (None).
        results = []
        for user_info in explicit_users:
            userId = user_info['id']
            user = mtool.getMemberById(userId)
            
            # ELAN ESD filter
            esd = user.getProperty("dp")
            if esd != self.context.UID():
                # print "passt nicht"
                continue
            
            # play safe, though this should never happen
            if user is None:
                logger.warn('Skipped user without principal object: %s' % userId)
                continue
            explicitlyAssignedRoles = []
            for rolemaker_id, rolemaker in rolemakers:
                # getRolesForPrincipal can return None
                roles = rolemaker.getRolesForPrincipal(user) or ()
                explicitlyAssignedRoles.extend(roles)

            roleList = {}
            for role in self.portal_roles:
                canAssign = user.canAssignRole(role)
                if role == 'Manager' and not self.is_zope_manager:
                    canAssign = False
                roleList[role]={'canAssign': canAssign,
                                'explicit': role in explicitlyAssignedRoles,
                                'inherited': role in allInheritedRoles.get(userId, [])}

            canDelete = user.canDelete()
            canPasswordSet = user.canPasswordSet()
            if ('Manager' in explicitlyAssignedRoles or
                'Manager' in allInheritedRoles.get(userId, [])):
                if not self.is_zope_manager:
                    canDelete = False
                    canPasswordSet = False

            user_info['roles'] = roleList
            user_info['login'] = user.getUserName()
            user_info['fullname'] = user.getProperty('fullname', '')
            user_info['email'] = user.getProperty('email', '')
            user_info['can_delete'] = canDelete
            user_info['can_set_email'] = user.canWriteProperty('email')
            user_info['can_set_password'] = canPasswordSet
            results.append(user_info)

        # Sort the users by fullname
        results.sort(key=lambda x: x is not None and x['fullname'] is not None and normalizeString(x['fullname']) or '')

        # Reset the request variable, just in case.
        self.request.set('__ignore_group_roles__', False)
        return results

class GroupDetailsControlPanel(UsersGroupsControlPanelView):

    def __call__(self):
        context = aq_inner(self.context)

        self.gtool = getToolByName(context, 'portal_groups')
        self.gdtool = getToolByName(context, 'portal_groupdata')
        self.regtool = getToolByName(context, 'portal_registration')
        self.groupname = getattr(self.request, 'groupname', None)
        self.grouproles = self.request.set('grouproles', [])
        self.group = self.gtool.getGroupById(self.groupname)
        self.grouptitle = self.groupname
        if self.group is not None:
            self.grouptitle = self.group.getGroupTitleOrName()

        self.request.set('grouproles', self.group.getRoles() if self.group else [])

        submitted = self.request.form.get('form.submitted', False)
        if submitted:
            CheckAuthenticator(self.request)

            msg = _(u'No changes made.')
            self.group = None

            title = self.request.form.get('title', None)
            description = self.request.form.get('description', None)
            addname = self.request.form.get('addname', None)


            if addname:
                if not self.regtool.isMemberIdAllowed(addname):
                    msg = _(u'The group name you entered is not valid.')
                    IStatusMessage(self.request).add(msg, 'error')
                    return self.index()

                # Modification for local user management
                esd = self.context
                prefix = esd.prefix or esd.getId()
                prefix = str(prefix)
                esd_title = esd.Title()
                
                addname = "%s_%s" % (prefix, addname)
                title = "%s (%s)" % (title, esd_title)

                props = {'title' : title, 'description': description, 'dp': esd.UID() }
                self.request.set("dp", esd.UID())
                print props
                success = self.gtool.addGroup(addname, 
                               properties=props, REQUEST=self.request)
#                success = self.gtool.addGroup(addname, (), (), title=title,
#                                              description=description,
#                                              properties=props,
#                                              REQUEST=self.request)
                if not success:
                    msg = _(u'Could not add group ${name}, perhaps a user or group with '
                            u'this name already exists.', mapping={u'name' : addname})
                    IStatusMessage(self.request).add(msg, 'error')
                    return self.index()

                self.group = self.gtool.getGroupById(addname)
                msg = _(u'Group ${name} has been added.',
                        mapping={u'name' : addname})

            elif self.groupname:
                self.gtool.editGroup(self.groupname, roles=None, groups=None,
                                     title=title, description=description,
                                     REQUEST=context.REQUEST)
                self.group = self.gtool.getGroupById(self.groupname)
                msg = _(u'Changes saved.')

            else:
                msg = _(u'Group name required.')

            processed = {}
            for id, property in self.gdtool.propertyItems():
                processed[id] = self.request.get(id, None)

            if self.group:
                # for what reason ever, the very first group created does not exist
                self.group.setGroupProperties(processed)

            IStatusMessage(self.request).add(msg, type=self.group and 'info' or 'error')
            if self.group and not self.groupname:
                target_url = '%s/%s' % (self.context.absolute_url(), '@@usergroup-groupprefs')
                self.request.response.redirect(target_url)
                return ''

        return self.index()


class GroupsOverviewControlPanel(GOCP):

    def doSearch(self, searchString):
        """ Search for a group by id or title"""
        acl = getToolByName(self, 'acl_users')
        rolemakers = acl.plugins.listPlugins(IRolesPlugin)

        searchView = getMultiAdapter((aq_inner(self.context), self.request), name='pas_search')

        # First, search for inherited roles assigned to each group.
        # We push this in the request so that IRoles plugins are told provide
        # the roles inherited from the groups to which the principal belongs.
        self.request.set('__ignore_group_roles__', False)
        self.request.set('__ignore_direct_roles__', True)
        inheritance_enabled_groups = searchView.merge(chain(*[searchView.searchGroups(**{field: searchString}) for field in ['id', 'title']]), 'id')
        allInheritedRoles = {}
        for group_info in inheritance_enabled_groups:
            groupId = group_info['id']
            group = acl.getGroupById(groupId)
            group_info['title'] = group.getProperty('title', group_info['title'])
            allAssignedRoles = []
            for rolemaker_id, rolemaker in rolemakers:
                # getRolesForPrincipal can return None
                roles = rolemaker.getRolesForPrincipal(group) or ()
                allAssignedRoles.extend(roles)
            allInheritedRoles[groupId] = allAssignedRoles

        # Now, search for all roles explicitly assigned to each group.
        # We push this in the request so that IRoles plugins don't provide
        # the roles inherited from the groups to which the principal belongs.
        self.request.set('__ignore_group_roles__', True)
        self.request.set('__ignore_direct_roles__', False)
        explicit_groups = searchView.merge(chain(*[searchView.searchGroups(**{field: searchString}) for field in ['id', 'title']]), 'id')

        # Tack on some extra data, including whether each role is explicitly
        # assigned ('explicit'), inherited ('inherited'), or not assigned at all (None).
        results = []
        for group_info in explicit_groups:
            groupId = group_info['id']
            group = acl.getGroupById(groupId)
            group_info['title'] = group.getProperty('title', group_info['title'])
            
            # ELAN ESD filter
            esd = group.getProperty("dp")
            if esd != self.context.UID():
                continue

            explicitlyAssignedRoles = []
            for rolemaker_id, rolemaker in rolemakers:
                # getRolesForPrincipal can return None
                roles = rolemaker.getRolesForPrincipal(group) or ()
                explicitlyAssignedRoles.extend(roles)

            roleList = {}
            for role in self.portal_roles:
                canAssign = group.canAssignRole(role)
                if role == 'Manager' and not self.is_zope_manager:
                    canAssign = False
                roleList[role]={'canAssign': canAssign,
                                'explicit': role in explicitlyAssignedRoles,
                                'inherited': role in allInheritedRoles.get(groupId, [])}

            canDelete = group.canDelete()
            if ('Manager' in explicitlyAssignedRoles or
                'Manager' in allInheritedRoles.get(groupId, [])):
                if not self.is_zope_manager:
                    canDelete = False

            group_info['roles'] = roleList
            group_info['can_delete'] = canDelete
            results.append(group_info)
        # Sort the groups by title
        sortedResults = searchView.sort(results, 'title')

        # Reset the request variable, just in case.
        self.request.set('__ignore_group_roles__', False)
        return sortedResults


class GroupMembershipControlPanel(UsersGroupsControlPanelView):

    def update(self):
        self.groupname = getattr(self.request, 'groupname')
        self.gtool = getToolByName(self, 'portal_groups')
        self.mtool = getToolByName(self, 'portal_membership')
        self.group = self.gtool.getGroupById(self.groupname)
        self.grouptitle = self.group.getGroupTitleOrName() or self.groupname

        self.request.set('grouproles', self.group.getRoles() if self.group else [])
        self.canAddUsers = True
        if 'Manager' in self.request.get('grouproles') and not self.is_zope_manager:
            self.canAddUsers = False

        self.groupquery = self.makeQuery(groupname=self.groupname)
        self.groupkeyquery = self.makeQuery(key=self.groupname)

        form = self.request.form
        submitted = form.get('form.submitted', False)

        self.searchResults = []
        self.searchString = ''
        self.newSearch = False

        if submitted:
            # add/delete before we search so we don't show stale results
            toAdd = form.get('add', [])
            if toAdd:
                if not self.canAddUsers:
                    raise Forbidden

                for u in toAdd:
                    self.gtool.addPrincipalToGroup(u, self.groupname, self.request)
                self.context.plone_utils.addPortalMessage(_(u'Changes made.'))

            toDelete = form.get('delete', [])
            if toDelete:
                for u in toDelete:
                    self.gtool.removePrincipalFromGroup(u, self.groupname, self.request)
                self.context.plone_utils.addPortalMessage(_(u'Changes made.'))

            search = form.get('form.button.Search', None) is not None
            edit = form.get('form.button.Edit', None) is not None and toDelete
            add = form.get('form.button.Add', None) is not None and toAdd
            findAll = form.get('form.button.FindAll', None) is not None and \
                not self.many_users
            # The search string should be cleared when one of the
            # non-search buttons has been clicked.
            if findAll or edit or add:
                form['searchstring'] = ''
            self.searchString = form.get('searchstring', '')
            if findAll or bool(self.searchString):
                self.searchResults = self.getPotentialMembers(self.searchString)

            if search or findAll:
                self.newSearch = True

        self.groupMembers = self.getMembers()

    def __call__(self):
        self.update()
        return self.index()

    def isGroup(self, itemName):
        return self.gtool.isGroup(itemName)

    def getMembers(self):
        searchResults = self.gtool.getGroupMembers(self.groupname)

        groupResults = [self.gtool.getGroupById(m) for m in searchResults]
        groupResults.sort(key=lambda x: x is not None and normalizeString(x.getGroupTitleOrName()))

        userResults = [self.mtool.getMemberById(m) for m in searchResults]
        userResults.sort(key=lambda x: x is not None and x.getProperty('fullname') is not None and normalizeString(x.getProperty('fullname')) or '')

        mergedResults = groupResults + userResults
        return filter(None, mergedResults)

    def getPotentialMembers(self, searchString):
        ignoredUsersGroups = [x.id for x in self.getMembers() + [self.group,] if x is not None]
        return self.membershipSearch(searchString, ignore=ignoredUsersGroups)

class UserMembershipControlPanel(UsersGroupsControlPanelView):

    def update(self):
        self.userid = getattr(self.request, 'userid')
        self.gtool = getToolByName(self, 'portal_groups')
        self.mtool = getToolByName(self, 'portal_membership')
        self.member = self.mtool.getMemberById(self.userid)

        form = self.request.form

        self.searchResults = []
        self.searchString = ''
        self.newSearch = False

        if form.get('form.submitted', False):
            delete = form.get('delete', [])
            if delete:
                for groupname in delete:
                    self.gtool.removePrincipalFromGroup(self.userid, groupname, self.request)
                self.context.plone_utils.addPortalMessage(_(u'Changes made.'))

            add = form.get('add', [])
            if add:
                for groupname in add:
                    group = self.gtool.getGroupById(groupname)
                    if 'Manager' in group.getRoles() and not self.is_zope_manager:
                        raise Forbidden

                    self.gtool.addPrincipalToGroup(self.userid, groupname, self.request)
                self.context.plone_utils.addPortalMessage(_(u'Changes made.'))

        search = form.get('form.button.Search', None) is not None
        findAll = form.get('form.button.FindAll', None) is not None and not self.many_groups
        self.searchString = not findAll and form.get('searchstring', '') or ''

        if findAll or not self.many_groups or self.searchString != '':
            self.searchResults = self.getPotentialGroups(self.searchString)

        if search or findAll:
            self.newSearch = True

        self.groups = self.getGroups()

    def __call__(self):
        self.update()
        return self.index()

    def getGroups(self):
        groupResults = [self.gtool.getGroupById(m) for m in self.gtool.getGroupsForPrincipal(self.member)]
        groupResults.sort(key=lambda x: x is not None and normalizeString(x.getGroupTitleOrName()))
        return filter(None, groupResults)

    def getPotentialGroups(self, searchString):
        ignoredGroups = [x.id for x in self.getGroups() if x is not None]
        return self.membershipSearch(searchString, searchUsers=False, ignore=ignoredGroups)
