from cgi import escape

try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
from zope.interface import implementer

from Products.CMFPlone.utils import safe_unicode

from interfaces import IDiscussion
from wsapi import WSAPI


@implementer(IDiscussion)
class Discussion(WSAPI):

    def get_discussion(self, path=''):
        """
        @param path - string to the path of the wanted object
        """
        obj = self.builder(self.context, path)
        portal_discussion = getSite().portal_discussion

        results = {}

        if portal_discussion.isDiscussionAllowedFor(obj):
            self.logger.info(
                "- get_discussion - Getting discussion for %s." %
                (obj))

            container = portal_discussion.getDiscussionFor(obj)

            for k, v in container.objectItems():
                results[k] = dict(
                    created=v.created().ISO(),
                    creators=v.creators,
                    title=safe_unicode(v.title),
                    text=safe_unicode(v.text),
                    cooked_text=escape(
                        safe_unicode(
                            v.cooked_text),
                        quote=True),
                    in_reply_to=v.in_reply_to or '',
                )

        return results
