from plone.supermodel import model
from zope import schema


class ISomeType(model.Schema):
    """
    """

    ScenarioCoordinates = schema.TextLine(
        title=u'Scenario coordinates',
        required=False,
    )

    area = schema.Text(
        title=u'Area coordinates',
        required=True,
    )
