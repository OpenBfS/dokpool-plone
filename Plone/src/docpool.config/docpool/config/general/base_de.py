from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from Products.PythonScripts.PythonScript import PythonScript

import transaction


def install(self):
    """
    """
    fresh = True
    if self.hasObject("config"):
        fresh = False  # It's a reinstall
    configUserFolders(self, fresh)
    createStructure(self, fresh)
    navSettings(self)
    createGroups(self)
    configureFiltering(self)
    setFrontpage(self)

# Further base structures


ADMINSTRUCTURE = [
    {
        TYPE: 'DPConfig',
        TITLE: 'Globale Konfiguration',
        ID: 'config',
        CHILDREN: [
            {
                TYPE: 'DocTypes',
                TITLE: 'Globale Dokumenttypen',
                ID: 'dtypes',
                CHILDREN: [],
            }
        ],
    }
]

# Configuration methods


def configUserFolders(self, fresh):
    """
    """
    # Turn creation of user folders on
    #    from plone.app.controlpanel.security import ISecuritySchema
    # Fetch the adapter
    from Products.CMFPlone.interfaces.controlpanel import ISecuritySchema

    security_adapter = ISecuritySchema(self)
    security_adapter.set_enable_user_folders(True)

    # Set type for user folders
    mtool = getToolByName(self, "portal_membership")
    mtool.setMemberAreaType("UserFolder")
    if fresh:
        mtool.addMember(
            'dpadmin',
            'Docpool Administrator (global)',
            ['Site Administrator', 'Member'],
            [],
        )
        dpadmin = mtool.getMemberById('dpadmin')
        dpadmin.setMemberProperties({"fullname": 'Docpool Administrator'})
        dpadmin.setSecurityProfile(password="admin")
        mtool.addMember(
            'dpmanager', 'Docpool Manager (global)', ['Manager', 'Member'], []
        )
        dpmanager = mtool.getMemberById('dpmanager')
        dpmanager.setMemberProperties({"fullname": 'Docpool Manager'})
        dpmanager.setSecurityProfile(password="admin")


def navSettings(self):
    IExcludeFromNavigation(self.news).exclude_from_nav = True
    self.news.reindexObject()
    IExcludeFromNavigation(self.events).exclude_from_nav = True
    self.events.reindexObject()
    IExcludeFromNavigation(self.Members).exclude_from_nav = True
    self.Members.reindexObject()


def createStructure(self, fresh):
    transaction.commit()
    createAdminstructure(self, fresh)
    transaction.commit()


def createAdminstructure(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, ADMINSTRUCTURE, fresh)


def setFrontpage(self):
    """
    """
    script_name = 'redirect'
    if script_name not in self.keys():
        self._setObject(script_name, PythonScript(script_name))
    ps = self._getOb(script_name)
    ps.write(
        """
if not context.isAdmin():
    container.REQUEST.RESPONSE.redirect(context.myFirstDocumentPool())
else:
    container.REQUEST.RESPONSE.redirect(context.absolute_url() + "/folder_contents")
"""
    )
    self.setLayout(script_name)


def configureFiltering(self):
    """
    """
    tid = 'safe_html'

    pt = getToolByName(self, 'portal_transforms')
    if not tid in pt.objectIds():
        return

    trans = pt[tid]

    tconfig = trans._config
    tconfig['class_blacklist'] = []
    tconfig['nasty_tags'] = {'meta': '1'}
    tconfig['remove_javascript'] = 0
    tconfig['stripped_attributes'] = [
        'lang',
        'valign',
        'halign',
        'border',
        'frame',
        'rules',
        'cellspacing',
        'cellpadding',
        'bgcolor',
    ]
    tconfig['stripped_combinations'] = {}
    tconfig['style_whitelist'] = [
        'text-align',
        'list-style-type',
        'float',
        'width',
        'height',
        'padding-left',
        'padding-right',
    ]  # allow specific styles for
    tconfig['valid_tags'] = {
        'code': '1',
        'meter': '1',
        'tbody': '1',
        'style': '1',
        'img': '0',
        'title': '1',
        'tt': '1',
        'tr': '1',
        'param': '1',
        'li': '1',
        'source': '1',
        'tfoot': '1',
        'th': '1',
        'td': '1',
        'dl': '1',
        'blockquote': '1',
        'big': '1',
        'dd': '1',
        'kbd': '1',
        'dt': '1',
        'p': '1',
        'small': '1',
        'output': '1',
        'div': '1',
        'em': '1',
        'datalist': '1',
        'hgroup': '1',
        'video': '1',
        'rt': '1',
        'canvas': '1',
        'rp': '1',
        'sub': '1',
        'bdo': '1',
        'sup': '1',
        'progress': '1',
        'body': '1',
        'acronym': '1',
        'base': '0',
        'br': '0',
        'address': '1',
        'article': '1',
        'strong': '1',
        'ol': '1',
        'script': '1',
        'caption': '1',
        'dialog': '1',
        'col': '1',
        'h2': '1',
        'h3': '1',
        'h1': '1',
        'h6': '1',
        'h4': '1',
        'h5': '1',
        'header': '1',
        'table': '1',
        'span': '1',
        'area': '0',
        'mark': '1',
        'dfn': '1',
        'var': '1',
        'cite': '1',
        'thead': '1',
        'head': '1',
        'hr': '0',
        'link': '1',
        'ruby': '1',
        'b': '1',
        'colgroup': '1',
        'keygen': '1',
        'ul': '1',
        'del': '1',
        'iframe': '1',
        'embed': '1',
        'pre': '1',
        'figure': '1',
        'ins': '1',
        'aside': '1',
        'html': '1',
        'nav': '1',
        'details': '1',
        'u': '1',
        'samp': '1',
        'map': '1',
        'object': '1',
        'a': '1',
        'footer': '1',
        'i': '1',
        'q': '1',
        'command': '1',
        'time': '1',
        'audio': '1',
        'section': '1',
        'abbr': '1',
        'strike': '1',
    }
    make_config_persistent(tconfig)
    trans._p_changed = True
    trans.reload()


def createGroups(self):
    gdata = getToolByName(self, 'portal_groupdata')
    try:
        gdata.manage_addProperty(
            "allowedDocTypes", "possibleDocTypes", "multiple selection"
        )
    except BaseException:
        pass
    try:
        gdata.manage_addProperty("dp", "possibleDocumentPools", "selection")
    except BaseException:
        pass
