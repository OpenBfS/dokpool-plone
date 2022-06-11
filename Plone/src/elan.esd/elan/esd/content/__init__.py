# For backward compatibility we need to have aliases for the former types
# for transfers
import sys

from docpool.event.content import dpevent, dpevents
from docpool.transfers.content import dptransferfolder, dptransfers

sys.modules["elan.esd.content.elantransferfolder"] = dptransferfolder
sys.modules["elan.esd.content.elantransfers"] = dptransfers
sys.modules["elan.esd.content.elanscenario"] = dpevent
sys.modules["elan.esd.content"].elanscenario = dpevent
sys.modules["elan.esd.content.elanscenarios"] = dpevents
sys.modules["elan.esd.content"].elanscenarios = dpevents
