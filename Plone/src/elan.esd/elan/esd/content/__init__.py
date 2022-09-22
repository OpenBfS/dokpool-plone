# For backward compatibility we need to have aliases for the former types
# for transfers
from docpool.base.content import dptransfersarea
from docpool.event.content import dpevent
from docpool.event.content import dpevents

import sys


sys.modules["elan.esd.content.elantransfers"] = dptransfersarea
sys.modules["elan.esd.content.elanscenario"] = dpevent
sys.modules["elan.esd.content"].elanscenario = dpevent
sys.modules["elan.esd.content.elanscenarios"] = dpevents
sys.modules["elan.esd.content"].elanscenarios = dpevents
