from AccessControl.SecurityInfo import allow_class
from docpool.base.appregistry import APP_REGISTRY
from plone.app.layout.viewlets.common import LogoViewlet
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from subprocess import check_output

import os
import plone.api as api
import shlex
import subprocess


class TimeViewlet(ViewletBase):
    index = ViewPageTemplateFile("time.pt")


allow_class(TimeViewlet)


class LogoDocpoolViewlet(LogoViewlet):

    index = ViewPageTemplateFile("logo.pt")

    def getActiveApp(self):
        user = api.user.get_current()
        if not user:
            return {}
        active_app = user.getProperty("apps")
        if not active_app:
            return {}
        return APP_REGISTRY[active_app[0]]

    def available(self):
        if api.user.is_anonymous():
            return False
        if api.portal.get_registry_record(name="docpool.show_debug_info"):
            return True

    def get_git_rev(self):
        # Git Revision
        commit_hash = os.getenv("GIT_COMMIT")
        if commit_hash:
            return commit_hash

        result = subprocess.run(
            shlex.split("git rev-parse --short HEAD"),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 128:
            return "Not detected"

        return result.stdout.strip()

    def get_git_branch(self):
        # Git Branch
        commit_name = os.getenv("GIT_REF_NAME")
        if commit_name:
            return commit_name

        result = subprocess.run(
            shlex.split("git rev-parse --abbrev-ref HEAD"),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 128:
            return "Not detected"

        return result.stdout.strip()
