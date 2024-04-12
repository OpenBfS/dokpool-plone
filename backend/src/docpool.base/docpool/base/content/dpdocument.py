from Acquisition import aq_get
from BTrees.OOBTree import OOBTree
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.archiving import IArchiving
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from docpool.base.content.extendable import Extendable
from docpool.base.marker import IImportingMarker
from docpool.base.pdfconversion import data
from docpool.base.pdfconversion import get_images
from docpool.base.pdfconversion import metadata
from docpool.base.pdfconversion import pdfobj
from docpool.base.utils import execute_under_special_role
from docpool.base.utils import portalMessage
from docpool.base.utils import queryForObject
from io import StringIO
from logging import getLogger
from PIL import Image
from plone import api
from plone import namedfile
from plone.api import content
from plone.app.contenttypes.content import Document
from plone.app.dexterity.textindexer.directives import searchable
from plone.app.discussion.interfaces import IConversation
from plone.app.textfield import RichText
from plone.app.textfield import RichTextValue
from plone.base.utils import safe_text
from plone.dexterity.content import Container
from plone.memoize import ram
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from zExceptions import BadRequest
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.container.interfaces import IContainerModifiedEvent
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
from zope.interface import implementer

import re


logger = getLogger(__name__)


def default_text():
    """This is a evil hack to work around https://redmine-koala.bfs.de/issues/3701 task
    3d. Rei-Reports do not want the text field which is required in the schema. By
    setting a default value for these the field can be hidden from the editor with css.
    """
    request = getRequest()
    if request and "reireport" in request.get("form.widgets.docType", []):
        return RichTextValue("REI-Bericht", "text/html", "text/x-html-safe")


class IDPDocument(IContentBase):
    """ """

    docType = schema.Choice(
        title=_("label_dpdocument_doctype", default="Document Type"),
        description=_("description_dpdocument_doctype", default=""),
        required=True,
        source="docpool.base.vocabularies.DocumentTypes",
    )

    searchable("text")
    text = RichText(
        title=_("label_dpdocument_text", default="Text"),
        description=_("description_dpdocument_text", default=""),
        defaultFactory=default_text,
        required=True,
    )


@implementer(IDPDocument)
class DPDocument(Container, Extendable, ContentBase):
    def change_state(self, id, action, REQUEST=None):
        """ """
        if REQUEST:
            alsoProvides(REQUEST, IDisableCSRFProtection)
        if not action:
            return self.restrictedTraverse("@@view")()
        doc = None
        try:
            doc = self._getOb(id)
        except BaseException:
            pass
        if doc:
            wftool = getToolByName(self, "portal_workflow")
            try:
                wftool.doActionFor(doc, action)
                if str(action) == "publish":
                    # when publishing we also publish any document inside the current
                    # document
                    for subdoc in doc.getDPDocuments():
                        try:
                            wftool.doActionFor(subdoc, action)
                        except BaseException:
                            pass
            except BaseException:
                return self.restrictedTraverse("@@view")()
            if REQUEST:
                portalMessage(self, _("The document state has been changed."), "info")
                return self.restrictedTraverse("@@view")()

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer.
        @return:
        """
        request = self.REQUEST
        dp_app_state = getMultiAdapter((self, request), name="dp_app_state")

        def _isClean():
            lbs = dp_app_state.appsEffectiveForObject(request)
            for lb in lbs:
                if not self.doc_extension(lb).isClean():
                    return False
            return self.unknownDocType() is None

        # We need to do this as Manager, because we need to check for all possible
        # reasons why a document could not by worked upon. Not just the reasons we
        # would be allowed to see as a user.
        return execute_under_special_role(self, "Manager", _isClean)

    def createActions(self):
        """
        We need to check if special workflows are needed depending on the user's role.
        """
        f = self.myFolderBase()
        r = api.user.get_roles(obj=f, inherit=True)
        if "Owner" in r:
            return
        if "Reviewer" in r:
            log("Setting Guest Workflow on Document " + self.getId())

            placeful_wf = getToolByName(self, "portal_placeful_workflow")
            try:
                self.manage_addProduct[
                    "CMFPlacefulWorkflow"
                ].manage_addWorkflowPolicyConfig()
            except BadRequest as e:
                log_exc(e)
            config = placeful_wf.getWorkflowPolicyConfig(self)
            placefulWfName = "dp-guest-document"
            config.setPolicyIn(policy=placefulWfName, update_security=False)
            config.setPolicyBelow(policy=placefulWfName, update_security=False)
            self.reindexObject()
            self.reindexObjectSecurity()

    def getAllowedSubTypes(self):
        dto = self.docTypeObj()
        if dto:
            adt = dto.allowedDocTypes
            if adt:
                return [dt.to_object for dt in adt]
        return []

    def customMenu(self, menu_items):
        """ """
        res1 = []
        if not self.uploadsAllowed():
            for menu_item in menu_items:
                if menu_item.get("id") in ["File", "Image"]:
                    continue
                res1.append(menu_item)
        else:
            res1 = menu_items
        dts = self.getAllowedSubTypes()
        res = []
        for menu_item in res1:
            if menu_item.get("id") == "DPDocument":
                for dt in dts:
                    action = "{}add++DPDocument?form.widgets.docType:list={}".format(
                        self.absolute_url(),
                        dt.id,
                    )
                    res.append(
                        {
                            "extra": {
                                "separator": None,
                                "id": dt.id,
                                "class": "contenttype-%s" % dt.id,
                            },
                            "submenu": None,
                            "description": "",
                            "title": safe_text(dt.Title),
                            "action": action,
                            "selected": False,
                            "id": dt.id,
                            "icon": None,
                        }
                    )
            else:
                res.append(menu_item)
        return res

    def allSubobjectsPublished(self):
        """

        @return:
        """
        for obj in self.getDPDocuments():
            if api.content.get_state(obj) != "published":
                return False
        return True

    def workflowActions(self):
        """ """
        wf_tool = getToolByName(self, "portal_workflow")
        workflowActions = wf_tool.listActionInfos(object=self)
        results = []
        for action in workflowActions:
            if action["category"] != "workflow":
                continue

            description = ""

            transition = action.get("transition", None)
            if transition is not None:
                description = transition.description

            if action["allowed"]:
                results.append(
                    {
                        "id": action["id"],
                        "title": action["title"],
                        "description": description,
                        "icon": action["id"] + ".png",
                    }
                )
        return results

    def unknownDocType(self):
        """
        If my doc type is in state private, return it.
        """
        dt = self.docTypeObj()
        if dt:
            tstate = api.content.get_state(dt)
            if tstate == "private":
                return dt
        return None

    def vocabDocType(self):
        """ """
        cat = getToolByName(self, "portal_catalog")
        types = cat(
            {
                "portal_type": "DocType",
                "sort_on": "sortable_title",
                "path": self.dpSearchPath(),
            }
        )
        return [(brain.id, brain.Title) for brain in types]

    def dp_type(self):
        """ """
        return self.docType

    def _docTypeObj_cachekey(method, self):
        if not self.id:
            # The object is being initialized
            return
        return (self.absolute_url_path(), self.modified())

    @ram.cache(_docTypeObj_cachekey)
    def docTypeObj(self):
        """ """
        if not self.id:
            # The object is being initialized
            return
        et = self.docType
        if not et:
            # The object is being saved and the attributes have not yet been saved
            et = self.REQUEST.get("form.widgets.docType", None)
            if et and isinstance(et, list):
                et = et[0]
        if not et:
            return
        # Uses Acquisition. Meh.
        config_folder = aq_get(self, "config", None)
        if not config_folder:
            logger.debug("No config folder for %s", self.absolute_url())
            return
        dto = config_folder["dtypes"].get(et, None)

        if not dto:
            logger.info("No DocType Object for type name '%s'", et)
        return dto

    def publishedImmediately(self, raw=False):
        """ """
        dto = self.docTypeObj()
        if dto:
            if not raw:
                # We only publish immediately when uploads are not allowed
                # and if we are not in a personal folder
                # print dto.publishImmediately, dto.allowUploads, self.isIndividual()
                return (
                    dto.publishImmediately
                    and not dto.allowUploads
                    and not self.isIndividual()
                )
            else:
                return dto.publishImmediately
        else:
            return False

    def uploadsAllowed(self):
        """ """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Add portal content", self):
            return False
        dto = self.docTypeObj()
        if dto:
            return dto.allowUploads
        else:
            return False

    def canBeDeleted(self):
        """ """
        mtool = getToolByName(self, "portal_membership")
        return mtool.checkPermission("Delete objects", self)

    def canBeEdited(self):
        """ """
        mtool = getToolByName(self, "portal_membership")
        return mtool.checkPermission("Modify portal content", self)

    def isInOneOfMyFolders(self):
        """
        Determine if the document is either in the users personal folder or in one of
        his groups. This should be defined by the Owner role on the object.
        """
        mtool = getToolByName(self, "portal_membership")
        return mtool.getAuthenticatedMember().has_role(
            "Owner", self
        ) or mtool.getAuthenticatedMember().has_role("Reviewer", self)

    def change_position(self, position, id, ptype):
        """
        Move a file or an image within the document.
        """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)
        position = position.lower()
        # we need to find all other ids for the same type
        ssids = [o.getId for o in self.getFolderContents({"portal_type": ptype})]
        # print ssids
        if position == "up":
            self.moveObjectsUp(id, 1, ssids)
        elif position == "down":
            self.moveObjectsDown(id, 1, ssids)
        self.plone_utils.reindexOnReorder(self)
        return self.restrictedTraverse("@@view")()

    def hasComments(self):
        """ """
        conversation = IConversation(self)
        return len(conversation.objectIds()) > 0

    def Identifier(self):
        """
        We offer this method here on the object, so that it is used by the RSS template.
        """
        dto = self.docTypeObj()
        if dto:
            cat = dto.contentCategory
            if cat:
                return "{}/@@dview?d={}&disable_border=1".format(
                    cat.absolute_url(),
                    self.UID(),
                )
        return self.absolute_url()

    def SearchableText(self):
        """
        We override, so we get the content of all subobjects indexed.
        """
        st = Document.SearchableText(self)  # TODO? searchable
        stsub = [obj.SearchableText() for obj in self.getAllContentObjects()]
        return st + " " + " ".join(stsub)

    def getRepresentativeImage(self):
        """ """
        dt = self.docTypeObj()
        if not dt:
            return None
        imgPattern = dt.imgPattern
        if imgPattern:
            p = re.compile(imgPattern, re.IGNORECASE)
            images = self.getImages()
            for image in images:
                if p.match(image.getId()):
                    return image
        else:
            return None

    def getRepresentativePDF(self):
        """ """
        dt = self.docTypeObj()
        if not dt:
            return None

        pdfPattern = dt.pdfPattern
        if pdfPattern:
            p = re.compile(pdfPattern, re.IGNORECASE)
            files = self.getFiles()
            for f in files:
                if p.match(f.getId()):
                    return f
        else:
            return None

    def generatePdfImage(self, pdffile):
        """ """
        pdf = pdfobj(pdffile)
        # Use BTrees
        storage = OOBTree()
        img = get_images(pdffile, 0, 1)
        storage["image_thumbnails"] = img
        meta = metadata(pdf)
        storage["metadata"] = meta

        annotations = IAnnotations(self)
        annotations["pdfimages"] = storage

        self.reindexObject()

    def pdfImage(self):
        """ """
        annotations = IAnnotations(self)
        if "pdfimages" in annotations:
            image = annotations["pdfimages"]["image_thumbnails"]["1_preview"]
            return image
        else:
            return None

    def autocreateSubdocuments(self):
        """
        TODO: specifically for XMLRPC usage
        """
        # * Von den allowed Types alle autocreatable Types durchgehen und ihre Muster
        #   "ausprobieren"
        # * Wenn Files oder Images gefunden zu einem Muster: entsprechendes DPDocument
        #   erzeugen und Files/Images verschieben
        return "ok"

    def setDPProperty(self, name, value, ptype="string"):
        """ """
        alsoProvides(self.REQUEST, IDisableCSRFProtection)
        if not self.hasProperty(name):
            self.manage_addProperty(name, value, ptype)
        else:
            self._updateProperty(name, value)
        return "set"

    def deleteDPProperty(self, name):
        """ """
        alsoProvides(self.REQUEST, IDisableCSRFProtection)
        if self.hasProperty(name):
            self._delProperty(name)
            return "deleted"
        return "unknown"

    def getDPProperty(self, name):
        """ """
        if self.hasProperty(name):
            return self.getProperty(name)

    def getDPProperties(self):
        """ """
        return self.propertyItems()

    def readPropertiesFromFile(self):
        """ """
        files = self.getFiles()
        msg = "none"
        for f in files:
            if f.getId() == "properties.txt":
                d = StringIO(data(f))
                props = d.readlines()
                for prop in props:
                    if prop and len(prop) > 2:
                        name, value = prop.split("=")
                        name = name.strip()
                        value = value.strip()
                        ptype = "string"
                        try:
                            name, ptype = name.split(":")
                        except BaseException:
                            pass
                        self.setDPProperty(name, value, ptype)
                        msg = "set"
        return msg

    def getFileOrImageByPattern(self, pattern):
        """ """
        #        print pattern
        #        print self.getAllContentObjects()
        p = re.compile(pattern, re.IGNORECASE)
        for obj in self.getAllContentObjects():
            #            print obj.getId()
            if p.match(obj.getId()):
                #                print obj
                return obj

    def getMapImageObj(self):
        """
        The map image is expected to be a file with with a name like 'xxx-map.png' or
        'yyy_map.jpg'.
        """
        return self.getFileOrImageByPattern(r".*[-_]map\..*")

    def getMapImage(self, scale=""):
        """ """
        img = self.getMapImageObj()
        if img:
            return f"<img src='{img.absolute_url()}{scale}' />"
        else:
            return _("No map image")

    def getLegendImageObj(self):
        """ """
        return self.getFileOrImageByPattern(r".*[-_]legend\..*")

    def getLegendImage(self, scale=""):
        """ """
        img = self.getLegendImageObj()
        if img:
            return f"<img src='{img.absolute_url()}{scale}' />"
        else:
            return _("No legend image")

    def getMyImage(self, refresh=False, full=True):
        """
        1. the map image, otherwise
        2. the representative image, otherwise
        3. try to generate an image from PDF
        4. Take the first image available in the doc
        5. a default image
        @param refresh: True --> generate afresh from PDF if necessary
        @param full: True --> combine map & legend images
        @return: a tuple with an image and a filename
        """
        alsoProvides(self.REQUEST, IDisableCSRFProtection)

        try:
            doc = self
            mapimg = self.getMapImageObj()
            if mapimg:
                legendimg = self.getLegendImageObj()
                dateiname = "{}.{}".format(mapimg.getId(), "png")
                if not full or not legendimg:
                    return mapimg.image.data, dateiname
                else:
                    # combine into one image if full=True and legend available
                    images = list(
                        map(
                            Image.open,
                            [
                                StringIO(mapimg.image.data),
                                StringIO(legendimg.image.data),
                            ],
                        )
                    )
                    w = sum(i.size[0] for i in images)
                    mh = max(i.size[1] for i in images)

                    result = Image.new("RGBA", (w, mh), "white")

                    x = 0
                    for i in images:
                        result.paste(i, (x, 0))
                        x += i.size[0]
                    res = StringIO()
                    result.save(res, "PNG")
                    return res.getvalue(), dateiname

            img = doc.getRepresentativeImage()
            if img:
                dateiname = "{}.{}".format(img.getId(), "png")
                return img.image.data, dateiname
            img = doc.pdfImage()
            if img and not refresh:
                dateiname = "{}.{}".format(img.getId(), "png")
                return img.data, dateiname

            pdf = doc.getRepresentativePDF()
            if pdf:
                execute_under_special_role(
                    doc, "Manager", DPDocument.generatePdfImage, doc, pdf
                )
                img = doc.pdfImage()
                dateiname = "{}.{}".format(img.getId(), "png")
                return img.data, dateiname

            img = doc.getFirstImageObj()
            if img:
                dateiname = "{}.{}".format(img.getId(), "png")
                return img.image.data, dateiname
        except Exception as e:
            log_exc(e)
            # TODO: Idea: support default image in DocType
            # Show Default image, if no other image is available
            img = self.restrictedTraverse(
                api.portal.get().absolute_url()
                + "/++plone++docpool.base/docdefaultimage.png"
            )
            return img().read(), "docdefaultimage.png"

    @property
    def image(self):
        """ """
        # We need to acquire Manager rights here, since we are called in traversal code,
        # which unfortunately comes as Anoymous
        result = execute_under_special_role(self, "Manager", self.getMyImage, False)
        if result:
            data, filename = result
            return namedfile.NamedImage(data, filename=safe_text(filename))

    def myState(self):
        """ """
        return content.get_state(self, "None")

    def getFirstImage(self, scale=""):
        img = self.getFirstImageObj()
        if img:
            return f"<img src='{img.absolute_url()}{scale}' />"
        else:
            return None

    def getFirstImageObj(self):
        """

        @return:
        """
        imgs = self.getImages()
        if imgs:
            img = imgs[0]
            return img
        else:
            return None

    def getLocalBehaviors(self):
        """

        :return:
        """
        from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport

        print(type(self.local_behaviors))
        print(self.local_behaviors)
        return ILocalBehaviorSupport(self).local_behaviors

    def myDPDocument(self):
        """ """
        return self

    def getFirstChild(self):
        """ """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """ """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getDPDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "DPDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getFiles(self, **kwargs):
        """ """
        args = {"portal_type": "File"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """ """
        args = {"portal_type": "Image"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    @property
    def allow_discussion(self):
        """Return commenting-setting of the docType unless archived.
        Uses a hack to re-add Acquisition since
        is_archive and docTypeObj both require it.
        """
        obj = api.content.get(UID=self.UID())
        if IArchiving(obj).is_archive:
            return False
        doc_type = obj.docTypeObj()
        return doc_type.allow_discussion_on_dpdocument if doc_type else False


@adapter(IDPDocument, IContainerModifiedEvent)
def updateContainerModified(obj, event=None):
    """ """
    if IImportingMarker.providedBy(getRequest()):
        return
    if not IArchiving(obj).is_archive:
        obj.update_modified()
        obj.reindexObject()  # New fulltext maybe needed
