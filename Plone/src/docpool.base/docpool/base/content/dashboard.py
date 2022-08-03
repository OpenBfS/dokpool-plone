from AccessControl import ClassSecurityInfo
from docpool.base import DocpoolMessageFactory as _
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface import implementer


class IDashboard(model.Schema):
    """ """

    dbCollections = RelationList(
        title=_("label_dashboard_dbcollections", default="Document Types"),
        description=_(
            "description_dashboard_dbcollections",
            default="Select the document types you want to show in this dashboard.",
        ),
        required=False,
        value_type=RelationChoice(
            title=_("Document Types"),
            source="docpool.base.vocabularies.DashboardCollections",
        ),
    )

    directives.widget(
        dbCollections="z3c.form.browser.select.CollectionSelectFieldWidget"
    )


@implementer(IDashboard)
class Dashboard(Item):
    """ """

    security = ClassSecurityInfo()

    def currentDocuments(self):
        """
        Loop through all configured collections,
        get the most recent document (if available).
        """
        res = []
        for c in self.dbCollections and self.dbCollections or []:
            coll = c.to_object
            docs = coll.results(b_size=1)
            if len(docs) > 0:
                res.append((coll.Title(), docs[0]))
            else:
                res.append((coll.Title(), None))
        #        print res
        return res
