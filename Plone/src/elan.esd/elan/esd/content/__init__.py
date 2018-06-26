##code-section main
# For backward compatibility we need to have aliases for the former types for transfers
import sys
from docpool.transfers.content import dptransferfolder
from docpool.transfers.content import dptransfers
sys.modules['elan.esd.content.elantransferfolder'] = dptransferfolder
sys.modules['elan.esd.content.elantransfers'] = dptransfers
##/code-section main 