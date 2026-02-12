from Products.Five.browser import BrowserView


class Overview(BrowserView):
    def __call__(self):
        return self.index()
