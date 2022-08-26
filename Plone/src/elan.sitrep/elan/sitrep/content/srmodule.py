#
# File: srmodule.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#
__author__ = ""
__docformat__ = "plaintext"

"""Definition of the SRModule content type. See srmodule.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from bs4 import BeautifulSoup
from DateTime import DateTime
from docpool.base.content.dpdocument import DPDocument
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.utils import back_references
from docpool.base.utils import portalMessage
from docpool.base.utils import queryForObjects
from docpool.elan.config import ELAN_APP
from elan.sitrep import DocpoolMessageFactory as _
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory
from plone.api import content
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.autoform import directives
from plone.base.utils import safe_text
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.protect.interfaces import IDisableCSRFProtection
from plone.subrequest import subrequest
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from urllib.parse import unquote
from urllib.parse import urljoin
from z3c.form.interfaces import IAddForm
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer

import requests


class ISRModule(model.Schema, IDPDocument):
    """ """

    directives.omitted(IAddForm, "text")

    currentReport = RelationChoice(
        title=_("label_srmodule_currentreport", default="Current report"),
        description=_(
            "description_srmodule_currentreport",
            default="If selected this report defines helpful defaults (text blocks, documents) for the content of this module.",
        ),
        required=False,
        source="elan.sitrep.vocabularies.CurrentReports",
    )

    docType = schema.Choice(
        title=_("label_srmodule_doctype", default="Module Type"),
        description=_("description_srmodule_doctype", default=""),
        required=True,
        source="elan.sitrep.vocabularies.ModuleTypes",
    )
    directives.widget(currentReport="z3c.form.browser.select.SelectFieldWidget")

    summary = RichText(
        title=_("label_srtextblock_summary", default="Summary"),
        description=_("description_srtextblock_summary", default=""),
        required=False,
    )


@implementer(ISRModule)
class SRModule(DPDocument):
    """ """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def createActions(self):
        super(DPDocument, self).createActions()
        df = self.defaultFilter()
        mc = df["config"]
        if mc:
            defaultTextBlocks = [tb.to_object for tb in (mc.defaultTextBlocks or [])]
            if defaultTextBlocks:
                text = ""
                for tb in defaultTextBlocks:
                    if tb.text:
                        text = text + safe_text(tb.text.output)
                self.text = RichTextValue(text, "text/html", "text/html")
                return
        self.text = RichTextValue(_("No information."), "text/plain", "text/html")

    def customMenu(self, menu_items):
        """ """
        return menu_items

    def getModuleTitle(self):
        """ """
        if self.currentReport:
            to_object_title = safe_text(self.currentReport.to_object.Title())
            self_title = safe_text(self.Title())

            return "{}: {} ({})".format(
                to_object_title,
                self_title,
                self.toLocalizedTime(DateTime(self.changed()), long_format=1),
            )
        else:
            return self.Title()

    def myReport(self):
        """ """
        if self.currentReport:
            return self.currentReport.to_object
        else:
            return None

    def previousVersions(self):
        """ """
        path = self.dpSearchPath()
        brains = queryForObjects(
            self,
            path=path,
            portal_type="SRModule",
            dp_type=self.docType,
            review_state="published",
            sort_on="changed",
            sort_order="reverse",
        )
        return brains

    def previousVersion(self):
        """
        The previous version is the instance youngest published instance of SRModule with the same Module Type.
        """
        pv = self.previousVersions()
        if len(pv) > 0:
            return pv[0].getObject()
        else:
            return None

    def defaultFilter(self):
        """
        Determines all default filter criteria for text blocks by looking at the currentReport and module type.
        """
        modType = self.docType
        res = {
            "scenario": None,
            "phase": None,
            "module_type": modType,
            "mandatory": False,
            "config": None,
        }
        r = self.myReport()
        if r:
            p = r.myPhaseConfig()
            if p:
                res["phase"] = p.getId()
                res["scenario"] = p.mySRScenario().getId()
                # my module is mandatory if the designated phase has a
                # moduleconfig for my type
                mcs = p.availableModuleConfigs()
                if mcs.get(modType, None):
                    res["mandatory"] = True
                    res["config"] = mcs.get(modType, None)
        return res

    def getFilter(self, request):
        """ """
        df = self.defaultFilter()
        scenario = request.get("scenario", df["scenario"])
        phase = request.get("phase", df["phase"])
        module_type = request.get("module_type", df["module_type"])
        return scenario, phase, module_type

    def possibleSRScenarios(self):
        """ """
        path = self.dpSearchPath()
        return [("", "---")] + [
            (brain.getId, brain.Title)
            for brain in queryForObjects(
                self, path=path, portal_type="SRScenario", sort_on="sortable_title"
            )
        ]

    def possibleSRPhases(self):
        """ """
        path = self.dpSearchPath()
        raw = queryForObjects(
            self, path=path, portal_type="SRPhase", sort_on="sortable_title"
        )
        ids = []
        res = []
        for p in raw:
            if p.getId in ids:
                continue
            else:
                ids.append(p.getId)
                res.append(p)
        return [("", "---")] + [(brain.getId, brain.Title) for brain in res]

    def possibleSRModuleTypes(self):
        """ """
        return [("", "---")] + ModuleTypesVocabularyFactory(self, raw=True)

    def usingReports(self):
        """
        Which reports am I being used in?
        """
        reports = back_references(self, "currentModules")
        return reports

    def visualisations(self):
        """ """
        sr_cat = getToolByName(self, "sr_catalog")
        df = self.defaultFilter()
        mc = df["config"]
        res = []
        if mc:
            res = mc.currentDocuments()[:20]
        if not mc:
            mc = []
            module_type = df["module_type"]
            mkbrains = sr_cat({"modules": module_type})
            for mkbrain in mkbrains:
                try:
                    res.extend(mkbrain.getObject().currentDocuments()[:20])
                except Exception as e:
                    print(e)
        if not res:
            mt = self.docTypeObj()
            if mt:
                res = mt.currentDocuments()[:20]
        return res

    def textBlocks(self):
        """ """
        request = self.REQUEST
        path = self.dpSearchPath()
        scenario, phase, module_type = None, None, None
        if request.get("filtered", False):
            scenario, phase, module_type = self.getFilter(request)
        else:
            df = self.defaultFilter()
            scenario = df.get("scenario", None)
            phase = df.get("phase", None)
            module_type = df.get("module_type", None)
            mc = df["config"]
            if mc:
                return mc.currentTextBlocks()
        args = {"portal_type": "SRTextBlock", "sort_on": "sortable_title", "path": path}
        if scenario:
            args["scenarios"] = scenario
        if phase:
            args["phases"] = phase
        if module_type:
            args["modules"] = module_type
        # print args
        sr_cat = getToolByName(self, "sr_catalog")
        brains = []
        ids = []
        if module_type:
            mkbrains = sr_cat({"modules": module_type})
            for mkbrain in mkbrains:
                try:
                    ids = sr_cat({"modules": mkbrain.getObject().getId()})
                    brains.extend(ids)
                except Exception as e:
                    print(e)
        if (scenario or phase) and module_type:
            brains = sr_cat(**args)
        return [brain.getObject() for brain in brains]

    def publishModule(self, justDoIt=False):
        """ """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)

        new_version = content.copy(source=self, id=self.getId(), safe_id=True)
        content.transition(new_version, transition="publish")
        if not justDoIt:
            portalMessage(self, _("The module has been published."), "info")
            return self.restrictedTraverse("@@view")()

    def docTypeObj(self):
        mt = self.dp_type()
        if (
            not mt
        ):  # The object is just being initialized and the attributes have not yet been saved
            mt = self.REQUEST.get("docType", "")
        # dto = queryForObject(self, id=et)
        dto = None
        #        print mt
        try:
            dto = self.config.mtypes[mt]
        except Exception as e:
            # et can be empty
            # print e
            pass
        if not dto:
            log("No ModuleType Object for type name '%s'" % self.dp_type())
        return dto

    def mySRModule(self):
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

    def getSRModules(self, **kwargs):
        """ """
        args = {"portal_type": "SRModule"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getTransferables(self, **kwargs):
        """ """
        args = {"portal_type": "Transferable"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(ISRModule, IEditFinishedEvent)
def updated(obj, event=None):
    log("SRModule updated: %s" % str(obj))
    # TODO:
    # read text, find all image links, replace with data URLs
    # find all html snippet links (marked with a css class), replace with html
    # content.
    html = obj.text and obj.text.output or ""
    if html:
        urltool = getToolByName(obj, "portal_url")
        portal = urltool.getPortalObject()
        portalbase = portal.absolute_url()
        base = obj.absolute_url() + "/"

        soup = BeautifulSoup(html)
        # first we handle all images
        for img in soup.findAll("img"):
            print(img)
            src = img["src"]
            if src.startswith("data"):
                continue
            # src might be relative
            absolute_src = join(base, src)
            # We convert the result of a request to the uri to a data URI
            new_uri = fetch_resources(portalbase, absolute_src)
            if new_uri:
                # and replace the original one
                img["src"] = new_uri

        for span in soup.findAll("span", {"class": "snippet"}):
            for anchor in span.findAll("a"):
                # print anchor
                href = anchor["href"]
                if ".." in href:
                    href = href.replace("/..", "")
                absolute_href = join(base, href)
                html_data = fetch_resources(
                    portalbase, absolute_href, resource_type="html"
                )
                if html_data:
                    ext_soup = BeautifulSoup(html_data)
                    body = ext_soup.find("body")
                    body = None
                    if body:
                        anchor.replaceWith(body)
                    else:
                        anchor.replaceWith(ext_soup)
        # finally we replace the html of the module with the manipulated
        # version
        new_html = str(soup)
        obj.text = RichTextValue(safe_text(new_html), "text/html", "text/html")


def join(base, url):
    """
    Join relative URL
    """
    if not (url.startswith("/") or "://" in url):
        return urljoin(base, url)
    else:
        # Already absolute
        return url


def fetch_resources(portalbase, uri, resource_type="image"):
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    """
    if uri.startswith(portalbase):
        response = subrequest(unquote(uri[len(portalbase) + 1 :]))
        if response.status != 200:
            return None
        ct = response.getHeader("content-type")
        data = response.getBody()
    else:
        response = requests.get(uri)
        if response.status_code != 200:
            return None
        ct = response.headers["content-type"]
        data = response.text
    if resource_type == "image":
        try:
            # stupid pisa doesn't let me send charset.
            ctype, encoding = ct.split("charset=")
            ctype = ctype.split(";")[0]
            # pisa only likes ascii css
            data = data.decode(encoding).encode("ascii", errors="ignore")

        except ValueError:
            ctype = ct.split(";")[0]

        data = data.encode("base64").replace("\n", "")
        data_uri = f"data:{ctype};base64,{data}"
        return data_uri
    else:
        return data
