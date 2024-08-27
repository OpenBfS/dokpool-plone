from AccessControl.SecurityInfo import allow_class
from App.config import getConfiguration
from docpool.base.appregistry import APP_REGISTRY
from logging import getLogger
from plone import api
from plone.app.layout.viewlets.common import LogoViewlet
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import datetime
import os
import shlex
import subprocess


logger = getLogger(__name__)


class TimeViewlet(ViewletBase):
    index = ViewPageTemplateFile("time.pt")

    def get_local_time(self):
        return datetime.datetime.now()

    def get_utc_time(self):
        return datetime.datetime.now(datetime.UTC)


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

    def read_git_version_file(self, filename):
        # Get the path to the pid file :)
        try:
            varbase = os.path.dirname(getConfiguration().pid_filename)
            project_root = os.path.abspath(os.path.join(varbase, ".."))
            file_path = os.path.join(project_root, filename)
        except AttributeError:
            # Ignore if we have no access to file
            logger.info("No version file_path found")
            return
        if not os.path.isfile(file_path):
            logger.info("No version file found")
            return

        with open(file_path) as file:
            content = file.read()
            if content:
                return content

    def get_git_rev(self):
        # Git Revision

        # If run inside docker with existing version file
        version_in_file = self.read_git_version_file("GIT_COMMIT")
        if version_in_file:
            return version_in_file

        # If run on the review server
        commit_hash = os.getenv("GIT_COMMIT")
        if commit_hash:
            return commit_hash

        # If run local
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
