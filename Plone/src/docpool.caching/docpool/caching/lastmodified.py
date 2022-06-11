from docpool.base.content.contentbase import IContentBase
from docpool.base.content.dpdocument import IDPDocument
from z3c.caching.interfaces import ILastModified
from zope.component import adapter
from zope.interface import implementer


@implementer(ILastModified)
@adapter(IContentBase)
class ContentBaseLastModified:
    """
    """

    def __init__(self, context):
        self.context = context

    def __call__(self):
        wdate = self.context.wdate
        modified = self.context.modified()
        if modified is not None:
            modified = modified.asdatetime()

        # no date?
        if wdate is None and modified is None:
            return None

        # both dates? we take the later date
        if wdate is not None and modified is not None:
            try:
                return wdate < modified and modified or wdate
            except BaseException:
                import pytz

                utc = pytz.UTC
                return (
                    wdate.replace(tzinfo=utc) < modified.replace(tzinfo=utc)
                    and modified
                    or wdate
                )

        # only one of them
        return wdate or modified


@implementer(ILastModified)
@adapter(IDPDocument)
class DocumentLastModified(ContentBaseLastModified):
    def __init__(self, context):
        super().__init__(context)

    def __call__(self):
        lm = super().__call__()
        # we need to consider date of last transfer
        transferred = None
        try:
            from docpool.transfers.behaviors.transferable import ITransferable

            t = ITransferable(self.context)
            tEvents = t.transferEvents()
            if len(tEvents) > 0:
                transferred = tEvents[0]['timeraw']
        except Exception as e:
            # log_exc(e)
            pass

        if lm is not None and transferred is not None:
            try:
                return lm < transferred and transferred or lm
            except BaseException:
                import pytz

                utc = pytz.UTC
                return (
                    lm.replace(tzinfo=utc) < transferred.replace(tzinfo=utc)
                    and transferred
                    or lm
                )

        # only one of them
        return lm or transferred
