from pathlib import Path
from plone import api
from plone.exportimport import logger
from plone.exportimport.exporters.principals import PrincipalsExporter
from plone.exportimport.utils import principals as principals_utils
from plone.exportimport.utils.principals.members import _get_base_user_data
from plone.exportimport.utils.principals.members import _get_user_password
from plone.exportimport.utils.principals.members import _get_user_properties
from plone.exportimport.utils.principals.members import _get_user_schema_fields


class CustomPrincipalsExporter(PrincipalsExporter):
    def dump(self) -> list[Path]:
        """Serialize object and dump it to disk."""
        data = {
            "groups": principals_utils.export_groups(),
            "members": export_members(),
        }
        filepath = self._dump(data, self.filepath)
        logger.debug(
            f"- Principals: Wrote {len(data['groups'])} groups and {len(data['members'])} members to {filepath}"
        )
        return [filepath]


def export_members() -> list[dict]:
    """Serialize all members as a list of dictionaries."""
    acl_users = api.portal.get_tool("acl_users")
    fields = _get_user_schema_fields()
    data = []
    users = [
        user
        for user in acl_users.searchUsers()
        if not user["pluginid"] == "mutable_properties"
    ]
    for user in users:
        user_id = user["userid"]
        member = api.user.get(user_id)
        # Base data
        user_data = _get_base_user_data(member)
        # Password
        user_data["password"] = _get_user_password(member)
        # Properties
        user_data.update(_get_user_properties(member, fields))
        # Add dokpool properties
        user_data["dp"] = member.getProperty("dp")
        data.append(user_data)
    return data
