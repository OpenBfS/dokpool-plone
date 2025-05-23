from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.extendable import Extendable
from docpool.base.utils import queryForObjects
from plone import api
from plone.autoform import directives
from plone.base.utils import safe_hasattr
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from Products.CMFPlone.utils import log
from z3c.form.browser.orderedselect import OrderedSelectFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import implementer


class IDocType(model.Schema):
    """ """

    allowUploads = schema.Bool(
        title=_(
            "label_doctype_allowuploads", default="Can contain documents and images"
        ),
        description=_("description_doctype_allowuploads", default=""),
        required=False,
        default=True,
    )

    publishImmediately = schema.Bool(
        title=_("label_doctype_publishimmediately", default="Publish immediately?"),
        description=_("description_doctype_publishimmediately", default=""),
        required=False,
        default=False,
    )

    globalAllow = schema.Bool(
        title=_(
            "label_doctype_globalallow",
            default="Can be used everywhere (not only as part of another type)",
        ),
        description=_("description_doctype_globalallow", default=""),
        required=False,
        default=True,
    )

    allow_discussion_on_dpdocument = schema.Bool(
        title=_(
            "label_doctype_allow_discussion",
            default="Allow commenting on this type",
        ),
        description="",
        required=False,
        default=False,
    )

    # TODO: This pattern allows to create relations to itself
    # Would it be better to not use relations here?
    allowedDocTypes = RelationList(
        title=_(
            "label_doctype_alloweddoctypes",
            default="Types are allowed as part of this type",
        ),
        description=_("description_doctype_alloweddoctypes", default=""),
        required=False,
        value_type=RelationChoice(
            vocabulary="docpool.base.vocabularies.DocType",
        ),
    )
    directives.widget("allowedDocTypes", OrderedSelectFieldWidget)

    partsPattern = schema.TextLine(
        title=_(
            "label_doctype_partspattern",
            default="Name pattern for files and images belonging to this type",
        ),
        description=_(
            "description_doctype_partspattern",
            default="Used for automatically creating objects of this type from collections of files and images.",
        ),
        required=False,
    )

    pdfPattern = schema.TextLine(
        title=_(
            "label_doctype_pdfpattern", default="Name pattern for representative PDF"
        ),
        description=_(
            "description_doctype_pdfpattern",
            default="If PDF exists, an image will be created from its first page as a visual representation for objects of this type.",
        ),
        required=False,
    )

    imgPattern = schema.TextLine(
        title=_(
            "label_doctype_imgpattern",
            default="Name pattern for representative image",
        ),
        description=_(
            "description_doctype_imgpattern",
            default="If image exists, it will be used as a visual representation for objects of this type.",
        ),
        required=False,
    )

    customViewTemplate = schema.TextLine(
        title=_("label_doctype_customviewtemplate", default="Custom View Template"),
        description=_("description_doctype_customviewtemplate", default=""),
        required=False,
    )


@implementer(IDocType)
class DocType(Container, Extendable):
    """ """


@adapter(IDocType, IEditFinishedEvent)
def updated(obj, event=None):
    log("DocType updated: %s" % str(obj))
    catalog = api.portal.get_tool("portal_catalog")
    mpath = "/"
    if safe_hasattr(obj, "dpSearchPath"):
        mpath = obj.dpSearchPath()
    brains = queryForObjects(
        obj,
        portal_type="DPDocument",
        path=mpath,
        dp_type=obj.getId(),
    )
    for brain in brains:
        try:
            # reindex object without changing the modification-date.
            log("Reindexing " + brain.getPath())
            catalog._reindexObject(brain.getObject(), idxs=["dp_type", "category"])
        except BaseException as e:
            log(e)
