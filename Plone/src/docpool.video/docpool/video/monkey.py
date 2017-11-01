# -*- coding: utf-8 -*- 
def getVideos(self, **kwargs):
    """
    """
    args = {'portal_type': 'WildcardVideo'}
    args.update(kwargs)
    return [obj.getObject() for obj in self.getFolderContents(args)]

