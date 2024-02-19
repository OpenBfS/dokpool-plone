from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFCore.utils import getToolByName
from z3c.relationfield.relation import RelationValue
from zope.component import getUtility
from zope.event import notify
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent


TYPE = "type"
TITLE = "title"
ID = "id"
CHILDREN = "children"
specialAttributes = (TYPE, TITLE, ID, CHILDREN)


def createPloneObjects(parent, definitions, fresh=False):
    """
    from plone.dexterity.utils import createContentInContainer
    """
    for objdef in definitions:
        title = objdef.get(TITLE)
        if ID in objdef:
            id = objdef[ID]
        else:
            id = ploneId(parent, title)
        #        print objdef
        #        print id
        #        print parent
        # Objekt erzeugen, wenn noch nicht vorhanden
        if not parent.hasObject(id):
            #            print parent
            parent.invokeFactory(id=id, type_name=objdef[TYPE], title=title)
            # print "createBasicPortalStructure - %s %s erzeugt" % (objdef[TYPE], id)
        else:
            # print "createBasicPortalStructure - %s %s bereits vorhanden" % (objdef[TYPE], id)
            if not fresh:
                if CHILDREN in objdef:
                    obj = parent._getOb(id)
                    createPloneObjects(obj, objdef[CHILDREN], fresh)
                continue  # Do not change objects. They might have been configured
        obj = parent._getOb(id)

        # Titel soll auf jeden Fall wie oben angegeben lauten
        #        if obj.Title()!=title:
        #            obj.setTitle(title)
        #            print "createBasicPortalStructure - %s %s - neuer Titel: '%s'" % (objdef[TYPE], id, title)
        obj.setTitle(title)

        # alle zusaetzlichen Attribute im Objekt setzen
        setAttributes(obj, objdef)
        notify(
            ObjectModifiedEvent(obj)
        )  # Otherwise relations will not be correctly indexed
        obj.reindexObject()
        # alle angegebenen Kinder erzeugen
        if CHILDREN in objdef:
            createPloneObjects(obj, objdef[CHILDREN], fresh)


def setAttributes(obj, objdef):
    from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport

    for attr in objdef:
        if not attr in specialAttributes:
            if attr[:4] == "ref_":  # references
                # print attr
                method = attr.split("_")[1]
                cat = getToolByName(obj, "portal_catalog")
                cat_values = cat(id=objdef[attr])

                intids = getUtility(IIntIds)
                values = []
                for brain in cat_values:
                    o = brain.getObject()
                    to_id = intids.getId(o)
                    rel = RelationValue(to_id)
                    values.append(rel)
                if not values:
                    print(
                        "No values {} configured for object {} ".format(
                            objdef[attr],
                            objdef,
                        )
                    )

                specialMethod = getattr(obj, method)
                if callable(specialMethod):
                    specialMethod(values)
                else:
                    setattr(obj, method, values)
            else:
                if (
                    attr == "setExcludeFromNav"
                    and IExcludeFromNavigation(obj, None) is not None
                ):
                    IExcludeFromNavigation(obj).exclude_from_nav = objdef[attr]
                elif attr == "local_behaviors":
                    lbs = ILocalBehaviorSupport(obj)
                    lbs.local_behaviors = objdef[attr]
                else:
                    # Dexterity based
                    setattr(obj, attr, objdef[attr])
    if (
        "setExcludeFromNav" not in objdef
        and IExcludeFromNavigation(obj, None) is not None
    ):
        # Workaround issue in folder_contents of Plone 6.0.0a6
        IExcludeFromNavigation(obj).exclude_from_nav = False


def ploneId(context, title):
    PLONE_UTILS = getToolByName(context, "plone_utils")
    return PLONE_UTILS.normalizeString(title)


def _setAllowedTypes(folder, types):
    """ """
    folder.setConstrainTypesMode(1)  # only explicitly allowed types
    folder.setLocallyAllowedTypes(types)


def _addAllowedTypes(folder, types):
    existing = folder.getLocallyAllowedTypes()
    existing.extend(types)
    new_types = list(set(existing))
    _setAllowedTypes(folder, new_types)


def set_local_roles(self, obj, userid, roles):
    prefix = self.prefix or self.getId()
    obj.manage_setLocalRoles(userid.format(prefix), roles)
