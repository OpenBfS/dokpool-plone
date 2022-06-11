from AccessControl.SecurityInfo import allow_module
from docpool.transfers import DocpoolMessageFactory as _
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@implementer(IVocabularyFactory)
class PermissionsVocabulary:
    """ """

    def __call__(self, context):
        return SimpleVocabulary(
            [
                SimpleTerm("write", title=_("write")),
                SimpleTerm("read/write", title=_("read/write")),
                SimpleTerm("suspend", title=_("suspended")),
            ]
        )


PermissionsVocabularyFactory = PermissionsVocabulary()


@implementer(IVocabularyFactory)
class UnknownOptionsVocabulary:
    """ """

    def __call__(self, context):
        return SimpleVocabulary(
            [
                SimpleTerm("block", title=_("don't accept")),
                SimpleTerm("confirm", title=_("needs confirmation")),
            ]
        )


UnknownOptionsVocabularyFactory = UnknownOptionsVocabulary()


@implementer(IVocabularyFactory)
class DTPermOptionsVocabulary:
    """ """

    def __call__(self, context):
        return SimpleVocabulary(
            [
                SimpleTerm("block", title=_("don't accept")),
                SimpleTerm("confirm", title=_("needs confirmation")),
                SimpleTerm("publish", title=_("publish immediately")),
            ]
        )


DTPermOptionsVocabularyFactory = DTPermOptionsVocabulary()


allow_module("docpool.transfers.vocabularies")
