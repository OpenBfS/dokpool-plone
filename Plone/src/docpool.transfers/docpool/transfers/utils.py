from plone import api


def is_sender(obj):
    roles = api.user.get_roles(obj=obj)
    if "Manager" in roles or "Site Administrator" in roles:
        return True
    groups = api.user.get_current().getGroups()
    for group in groups:
        if "Senders" in group:
            return True
    return False
