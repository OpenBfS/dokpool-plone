"""Common configuration constants"""

PROJECTNAME = "docpool.base"


BASE_APP = "base"
TRANSFERS_APP = "transfers"

FOLDER_TYPES = [
    "CollaborationFolder",
    "ContentArea",
    "DPTransferFolder",
    "DPTransfersArea",
    "ELANInfos",
    "Folder",
    "GroupFolder",
    "Groups",
    "InfoFolder",
    "PrivateFolder",
    "ReviewFolder",
    "SimpleFolder",
    "UserFolder",
    "Users",
]

# These types are listed in Folder-Types as
OTHER_TYPES = [
    "Collection",
    "Document",
    "Event",
    "File",
    "Image",
    "InfoDocument",
    "InfoLink",
    "Link",
    "News Item",
    "Text",
]

JOURNAL_FOLDER_ID = "journal"
JOURNALENTRY_ID = "journalentry"

PRIVATE_STATES = ["private"]
PENDING_STATES = [
    "pending",
    "pending_authority",
    "pending_bfs",
    "pending_bmu",
    "pending_second",
]
PUBLISHED_STATES = ["published"]
REVISED_STATES = ["revised"]
