# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr

from docpool.base.appregistry import registerApp
from docpool.config.local.elan import dpAdded, dpRemoved
from docpool.elan.config import ELAN_APP
from docpool.elan.behaviors.elandoctype import IELANDocType
from docpool.elan.behaviors.elandocument import IELANDocument


registerApp(ELAN_APP, u"ELAN", IELANDocType, IELANDocument, dpAdded, dpRemoved, "elan_app_icon.png")