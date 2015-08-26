# -*- coding: utf-8 -*-

from zope.lifecycleevent import ObjectModifiedEvent
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue
from zope.event import notify
from Products.CMFCore.utils import getToolByName


TYPE='type'
TITLE='title'
ID='id'
CHILDREN='children'
specialAttributes=(TYPE, TITLE, ID, CHILDREN)


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
        print objdef
        print id
        print parent    
        # Objekt erzeugen, wenn noch nicht vorhanden
        if (not parent.hasObject(id)):
            print parent
            parent.invokeFactory(id=id, type_name=objdef[TYPE], title=title)
            print "createBasicPortalStructure - %s %s erzeugt" % (objdef[TYPE], id)
        else:
            print "createBasicPortalStructure - %s %s bereits vorhanden" % (objdef[TYPE], id)
            if not fresh:
                if CHILDREN in objdef:
                    obj = parent._getOb(id)
                    createPloneObjects(obj, objdef[CHILDREN], fresh)
                continue # Do not change objects. They might have been configured
        obj = parent._getOb(id)
        
        # Titel soll auf jeden Fall wie oben angegeben lauten
#        if obj.Title()!=title:
#            obj.setTitle(title)
#            print "createBasicPortalStructure - %s %s - neuer Titel: '%s'" % (objdef[TYPE], id, title)
        obj.setTitle(title)
            
        # alle zusaetzlichen Attribute im Objekt setzen
        setAttributes(obj, objdef)
        notify(ObjectModifiedEvent(obj)) # Otherwise relations will not be correctly indexed
        obj.reindexObject()
        # alle angegebenen Kinder erzeugen
        if CHILDREN in objdef:
            createPloneObjects(obj, objdef[CHILDREN], fresh)
    
def setAttributes(obj, objdef):
    for attr in objdef:
        if not attr in specialAttributes:
            if attr[:4] == "ref_": # references
                #print attr
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
                    print "No values %s configured for object %s " % (objdef[attr], objdef)
                
                getattr(obj,method)(values)
            else:
                #print obj.id, attr, objdef[attr]
                #print obj
                if obj.getPortalTypeName() in ['TemplatedDocument']:
                    #Archetypes based
                    setter = getattr(obj, attr)
                    setter(objdef[attr])
                else:
                    #Dexterity based
                    setattr(obj, attr, objdef[attr])
    


    
def ploneId(context, title):
    PLONE_UTILS=getToolByName(context, 'plone_utils')
    return PLONE_UTILS.normalizeString(title)
 

def _setAllowedTypes(folder, types):
    """
    """
    folder.setConstrainTypesMode(1) # only explicitly allowed types
    folder.setLocallyAllowedTypes(types)      