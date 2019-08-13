from zope.i18nmessageid import message
from zope.interface import implementer
from six.moves.xmlrpc_client import DateTime as XMLRPCDateTime

from DateTime import DateTime
from wsapi4plone.core.interfaces import IScrubber
import six


@implementer(IScrubber)
class Scrubber(object):

    def dict_scrub(self, data):
        """
        This method will scrub a the 'data' dictionary of any values that can not
        be marshalled (e.g. i18n Messages). Additionally it prepares all the key
        value pairs for transport by converting all strings to unicode.

        @param data - dictionary to be scrubbed

        DocTest
        -------
        We need to create some example data

            >>> msg = message.Message("hello world")
            >>> text1 = "hallo welt" # german
            >>> text2 = u"bonjour tout le monde" # french
            >>> dict1 = {'spring': 'slinky', 'stick': u'cue'}

        Now from this example data we would the dictionary to hand to dict_scrub

            >>> ddata = {'greeting': msg, 'sometext': text1, 'moretext': text2, 'misc': dict1}

        Run it though the dictionary scrubber

            >>> Scrubber.dict_scrub(Scrubber(), ddata)
            {'misc': {'spring': 'slinky', 'stick': u'cue'}, 'greeting': u'hello world', 'moretext': u'bonjour tout le monde', 'sometext': 'hallo welt'}
        """
        # TODO pumazi: add language support (il8n)
        results = {}
        for k in data:
            # if type(data[k]) == str:
            #     results[unicode(k)] = unicode(data[k], 'utf-8')
            # elif type(data[k]) == message.Message:
            #     results[unicode(k)] = unicode(data[k].encode('utf-8'))
            # elif type(data[k]) == dict:
            #     results[unicode(k)] = self.dict_scrub(data[k])
            # else:
            #     results[unicode(k)] = data[k]
            if isinstance(data[k], message.Message):
                results[k] = six.text_type(data[k].encode('utf-8'))
            elif isinstance(data[k], dict):
                results[k] = self.dict_scrub(data[k])
            elif isinstance(data[k], DateTime):  # correct DateTime values
                results[k] = XMLRPCDateTime(data[k])
            else:
                results[k] = data[k]
        return results


def scrub():
    return Scrubber()
