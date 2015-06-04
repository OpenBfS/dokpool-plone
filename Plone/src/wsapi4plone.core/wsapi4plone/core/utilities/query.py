from zope.component import getUtility
from zope.interface import implements

import Missing

from wsapi4plone.core.interfaces import IFormatQueryResults, IScrubber


class FormatQueryResults(object):
    implements(IFormatQueryResults)

    masking = {'cmf_uid': None,
               'exclude_from_nav': None,
               'getIcon': None,
               'getId': None,
               'getObjSize': 'size',
               'is_folderish': 'container',
               'meta_type': None,
               'portal_type': None, # redundant data, would seem to correspond with 'Type'
              }

    def __call__(self, brains):
        grey_matter = {}
        for brain in brains:
            path = brain.getPath()
            grey_matter[path] = {}
            for neuron in brain.schema():
                if brain[neuron] == Missing.Value:
                    continue
                elif neuron in self.masking.keys():
                    if self.masking[neuron]:
                        grey_matter[path][self.masking[neuron]] = brain[neuron]
                    else: continue
                else:
                    grey_matter[path][neuron] = brain[neuron]
        scrubber = getUtility(IScrubber)
        jarred_brains = scrubber.dict_scrub(grey_matter)
        return jarred_brains


def formatter():
    return FormatQueryResults()
