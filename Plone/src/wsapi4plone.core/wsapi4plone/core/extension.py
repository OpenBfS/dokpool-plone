# -*- coding: utf-8 -*-
from wsapi4plone.core.interfaces import ICallbackExtension, IWriteExtension
from wsapi4plone.core.exceptions import ReadOnlyException


class BaseExtension(object):
    """Base extension."""

    def __init__(self, service, context):
        self.service = service
        self.context = context
        if hasattr(self, 'update') and \
           callable(getattr(self, 'update', None)):
            self.update()

    @property
    def provides_callback(self):
        return ICallbackExtension.providedBy(self)

    def get(self):
        raise NotImplementedError(
            "%s does not implement the get_extension method. This extension "
            "has adapted %s and %s." % (self.__class__.__name__, self.service,
            self.context))


class BaseWriteExension(object):
    """Base write extension."""

    def set(self, **kwargs):
        name = self.__class__.__name__
        if not IWriteExtension.providedBy(self):
            raise ReadOnlyException("%s is a read-only extension." % name)
        else:
            raise NotImplementedError(
                "%s does not implement the set_extension method. This "
                "extension has adapted %s and %s." % (name, self.service,
                self.context))

    def get_skeleton(self):
        raise NotImplementedError(
            "%s does not implement the get_skeleton method. This extension "
            "has adapted %s and %s." % (self.__class__.__name__, self.service,
            self.context))
