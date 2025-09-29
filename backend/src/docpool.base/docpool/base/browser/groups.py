from operator import itemgetter
from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import logging


log = logging.getLogger(__name__)
LDAP_PREFIX = "Plone-"


class GroupsListing(BrowserView):
    """Display all Groups with information about members, source, roles and
    groups they are members of.
    """

    def get_groups(self):
        results = []
        group_tool = api.portal.get_tool("portal_groups")
        for group in group_tool.listGroups():
            if group.id == "AuthenticatedUsers":
                continue
            groups = []
            users = []
            for member in group.getGroupMembers():
                if group_tool.isGroup(member):
                    groups.append((member.id, member.getGroupTitleOrName()))
                else:
                    users.append((member.id, member.getProperty("fullname")))
            member_in = group_tool.getGroupsForPrincipal(group)
            try:
                member_in.remove("AuthenticatedUsers")
            except ValueError:
                pass
            roles = group.getRoles()
            try:
                roles.remove("Authenticated")
            except ValueError:
                pass
            local_roles = api.group.get_roles(group=group, obj=self.context)
            try:
                local_roles.remove("Authenticated")
            except ValueError:
                pass
            local_roles = set(local_roles) - set(roles)

            ldap = False  # is_ldap_group(group=group)
            if ldap and has_ldap_prefix(group=group):
                sortkey = group.id[len(LDAP_PREFIX) :] + "zzz"
            else:
                sortkey = group.id
            groupinfo = {
                "id": group.id,
                "title": group.getGroupTitleOrName(),
                "groups": groups,
                "users": users,
                "roles": roles,
                "local_roles": set(local_roles) - set(roles),
                "member_in": member_in,
                "ldap": ldap,
                "sortkey": sortkey,
            }
            results.append(groupinfo)
        return sorted(results, key=itemgetter("sortkey"))


class GroupMembersFlattened(BrowserView):
    template = ViewPageTemplateFile("templates/group_members_flattened.pt")

    def __call__(self, groupname=None):
        if not groupname:
            return
        self.members = flatten_members([groupname])
        self.grouptitle = api.group.get(groupname).getGroupTitleOrName()
        return self.template()


def is_ldap_group(group=None, groupid=None):
    if groupid and not group:
        group = api.group.get(groupid)
    actual = group.getGroup()
    return "pasldap" in actual._propertysheets


def has_ldap_prefix(group=None, groupid=None):
    if group and not groupid:
        groupid = group.id
    return groupid.startswith(LDAP_PREFIX)


def flatten_members(names, memberdata=False):
    """
    Recursively get a list of member-id's from a list of principals.
    :param name: names (a list of names of users or groups)
    :return: set of member-id's
    """
    if not isinstance(names, (list, tuple, set)):
        names = [names]
    group_tool = api.portal.get_tool(name="portal_groups")
    portal_membership = api.portal.get_tool("portal_membership")
    member_list = []

    for name in names:
        if not name or name in member_list:
            continue
        name = cleanup_name(name)
        user = portal_membership.getMemberById(name)
        if user:
            if memberdata:
                member_list.append(user)
            else:
                member_list.append(name)
            continue

        group = group_tool.getGroupById(name)
        if not group:
            log.warn(f"Group {name} not found")
            continue

        for member in group.getGroupMembers():
            if group_tool.isGroup(member):
                members = flatten_members([member.id], memberdata=memberdata)
                member_list.extend(members)
            else:
                if memberdata:
                    member_list.append(member)
                else:
                    member_list.append(member.id)
    return set(member_list)


def cleanup_name(name):
    """Remove leading 'user:' and 'group:' prefixes added by the
    principals-vocabulary"""
    if name is None:
        return name
    if name.startswith("user:"):
        name = name[5:]
    elif name.startswith("group:"):
        name = name[6:]
    return name
