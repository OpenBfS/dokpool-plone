from plone import api
from plone.exportimport import logger
from plone.exportimport.importers.principals import PrincipalsImporter
from plone.exportimport.utils import principals as principals_utils
from Products.PlonePAS.tools.groupdata import GroupData
from typing import List


class CustomPrincipalsImporter(PrincipalsImporter):
    name: str = "principals"

    def _import_groups(self, groups=List[dict]) -> int:
        logger.debug(f"- Principals: Read {len(groups)} groups from {self.filepath}")
        total = len(import_groups(groups))
        logger.debug(f"- Principals: Imported {total} groups")
        return total

    def _import_members(self, members=List[dict]) -> int:
        logger.debug(f"- Principals: Read {len(members)} groups from {self.filepath}")
        # Change: Exclude existing members
        members = [m for m in members if not api.user.get(username=m["username"])]
        total = len(principals_utils.import_members(members))
        logger.debug(f"- Principals: Imported {total} members")
        return total


def import_groups(data: List[dict]) -> List[GroupData]:
    """Import groups."""
    groups = []
    acl = api.portal.get_tool("acl_users")
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
                pass

        # Change: Add docpool props
        props = {}
        if item.get("allowedDocTypes") not in [None, [""], []]:
            props["allowedDocTypes"] = item["allowedDocTypes"]
        if item.get("dp"):
            props["dp"] = item["dp"]
        if props:
            group.setGroupProperties(props)

    return groups
