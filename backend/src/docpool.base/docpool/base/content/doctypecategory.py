from docpool.base import DocpoolMessageFactory as _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IDocTypeCategory(model.Schema):
    """ """

    icon_name = schema.Choice(
        title=_("label_doctype_icon_name", default="Icon Name"),
        description=_(
            "description_doctypecategory_icon_name",
            default="Name of a icon (see https://icons.getbootstrap.com for reference)",
        ),
        vocabulary="docpool.base.vocabularies.Icons",
        default="bookmark",
        required=False,
    )
    directives.widget("icon_name", SelectFieldWidget)


@implementer(IDocTypeCategory)
class DocTypeCategory(Container):
    """ """

    APP = "base"
