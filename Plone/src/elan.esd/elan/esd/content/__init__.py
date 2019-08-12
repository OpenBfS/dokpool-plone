# For backward compatibility we need to have aliases for the former types for transfers
from docpool.event.content import dpevent
from docpool.event.content import dpevents
from docpool.transfers.content import dptransferfolder
from docpool.transfers.content import dptransfers

import sys


sys.modules['elan.esd.content.elantransferfolder'] = dptransferfolder
sys.modules['elan.esd.content.elantransfers'] = dptransfers
sys.modules['elan.esd.content.elanscenario'] = dpevent
sys.modules['elan.esd.content'].elanscenario = dpevent
sys.modules['elan.esd.content.elanscenarios'] = dpevents
sys.modules['elan.esd.content'].elanscenarios = dpevents
