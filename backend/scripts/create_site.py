from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from Testing.makerequest import makerequest

import logging
import os
import transaction

logging.basicConfig(format="%(message)s")

# Silence some loggers
for logger_name in [
    "GenericSetup.componentregistry",
    "Products.MimetypesRegistry.MimeTypesRegistry",
]:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

logger = logging.getLogger("Plone Site Creation")
logger.setLevel(logging.DEBUG)

truthy = frozenset(("t", "true", "y", "yes", "on", "1"))


def asbool(s):
    """Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is a :term:`truthy string`. If ``s`` is already one of the
    boolean values ``True`` or ``False``, return it."""
    if s is None:
        return False
    if isinstance(s, bool):
        return s
    s = str(s).strip()
    return s.lower() in truthy


DELETE_EXISTING = asbool(os.getenv("DELETE_EXISTING"))
EXAMPLE_CONTENT = asbool(
    os.getenv("EXAMPLE_CONTENT", "1")
)  # Create example content by default

app = makerequest(globals()["app"])

request = app.REQUEST

# ifaces = [IBrowserLayer]
# for iface in directlyProvidedBy(request):
#     ifaces.append(iface)

# directlyProvides(request, *ifaces)

admin = app.acl_users.getUserById("admin")
admin = admin.__of__(app.acl_users)
newSecurityManager(None, admin)

site_id = "Plone"
payload = {
    "title": "Dokpool Demo",
    "profile_id": _DEFAULT_PROFILE,
    "distribution_name": "docpooldemo",
    "setup_content": True,
    "default_language": "de",
    "portal_timezone": "Europe/Berlin",
}

logger.info(f"Creating a new Plone site {site_id}")

if site_id in app.objectIds() and DELETE_EXISTING:
    app.manage_delObjects([site_id])
    transaction.commit()
    app._p_jar.sync()
elif site_id in app.objectIds() and not DELETE_EXISTING:
    logger.info(
        f" - Stopping site creation, as there is already a site with id {site_id} at the instance. "
        "Set DELETE_EXISTING=1 to delete the existing site before creating a new one."
    )

if site_id not in app.objectIds():
    site = addPloneSite(app, site_id, **payload)
    transaction.commit()
    app._p_jar.sync()
    logger.info(" - Site created!")
