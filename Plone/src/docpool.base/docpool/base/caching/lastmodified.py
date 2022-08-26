from datetime import timezone
from docpool.base.content.contentbase import IContentBase
from docpool.base.content.dpdocument import IDPDocument
from z3c.caching.interfaces import ILastModified
from zope.component import adapter
from zope.interface import implementer


def maxdate(*dates):
    if not (dates := [date for date in dates if date is not None]):
        return

    try:
        return max(dates)
    except TypeError:
        return max(date.replace(tzinfo=timezone.utc) for date in dates)
    else:
        return dates[0]


@implementer(ILastModified)
@adapter(IContentBase)
class ContentBaseLastModified:
    def __init__(self, context):
        self.context = context

    def __call__(self):
        wdate = self.context.wdate
        modified = self.context.modified()
        if modified is not None:
            modified = modified.asdatetime()
        return maxdate(wdate, modified)


@adapter(IDPDocument)
class DocumentLastModified(ContentBaseLastModified):
    def __call__(self):
        lm = super().__call__()

        # we need to consider date of last transfer
        transferred = None
        try:
            from docpool.transfers.behaviors.transferable import ITransferable

            t = ITransferable(self.context)
        except Exception:
            pass
        else:
            if tEvents := t.transferEvents():
                transferred = tEvents[0]["timeraw"]

        return maxdate(lm, transferred)
