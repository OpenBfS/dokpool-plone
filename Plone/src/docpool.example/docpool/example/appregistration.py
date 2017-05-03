# -*- coding: utf-8 -*-

from docpool.base.appregistry import registerApp
# This logic should eventually be bundled in the global docpool.config module to allow for easy customization
from docpool.example.local.example import dpAdded, dpRemoved
from docpool.example.behaviors.exampledoc import IExampleDoc
from docpool.example.behaviors.exampletype import IExampleType
from docpool.example.config import EXAMPLE_APP

# TODO: register any app specific type extension, doc extension, methods to be executed when docpools are created
registerApp(EXAMPLE_APP, u"Example App", IExampleType, IExampleDoc, dpAdded, dpRemoved, icon="example_app_icon.png", implicit=False)