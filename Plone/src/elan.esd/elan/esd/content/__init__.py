##code-section main
# For backward compatibility we need to have aliases for the former types for transfers
import sys
from docpool.transfers.content.dptransferfolder import DPTransferFolder
from docpool.transfers.content.dptransfers import DPTransfers
sys.modules['elan.esd.content.elantransferfolder.ELANTransferFolder'] = DPTransferFolder
sys.modules['elan.esd.content.elantransfers.ELANTransfers'] = DPTransfers
##/code-section main 