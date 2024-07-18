from plone import api
from plone.exportimport import logger
from plone.exportimport.importers.principals import PrincipalsImporter
from plone.exportimport.utils import principals as principals_utils
from Products.PlonePAS.tools.groupdata import GroupData


class CustomPrincipalsImporter(PrincipalsImporter):
    name: str = "principals"

    def _import_groups(self, groups=list[dict]) -> int:
        logger.debug(f"- Principals: Read {len(groups)} groups from {self.filepath}")
        total = len(import_groups(groups))
        logger.debug(f"- Principals: Imported {total} groups")
        return total

    def _import_members(self, members=list[dict]) -> int:
        logger.debug(f"- Principals: Read {len(members)} groups from {self.filepath}")
        # Change: Exclude existing members
        members = [m for m in members if not api.user.get(username=m["username"])]
        total = len(principals_utils.import_members(members))
        logger.debug(f"- Principals: Imported {total} members")
        return total


def import_groups(data: list[dict]) -> list[GroupData]:
    """Import groups."""
    groups = []
    not_found_pricipals = []
    acl = api.portal.get_tool("acl_users")
    portal_groups = api.portal.get_tool("portal_groups")
    groupsIds = {item["id"] for item in acl.searchGroups()}
    for item in data:
        groupid = item["groupid"]
        principals = item.pop("principals", [])
        if groupid not in groupsIds:
            group = api.group.create(
                groupname=groupid,
                title=item["title"],
                description=item["description"],
                roles=item["roles"],
            )
            groups.append(group)
        else:
            group = api.group.get(groupname=groupid)
        # add all principals, even if they are not stored in plone (e.g. LDAP)
        for principal in principals:
            try:
                api.group.add_user(group=group, username=principal)
            except api.exc.UserNotFoundError:
                # A principal may be a group created after this one. We defer and try again.
                not_found_pricipals.append({"group": groupid, "principal": principal})
                pass

        # Change: Add docpool props
        props = {}
        if item.get("allowedDocTypes") not in [None, [""], []]:
            props["allowedDocTypes"] = item["allowedDocTypes"]
        if item.get("dp"):
            props["dp"] = item["dp"]
        if props:
            group.setGroupProperties(props)

    # Try again to to add groups that dod not exists before
    for item in not_found_pricipals:
        if api.group.get(groupname=item["group"]):
            portal_groups.addPrincipalToGroup(item["principal"], item["group"])

    return groups
