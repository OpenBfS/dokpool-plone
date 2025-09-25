from docpool.base.behaviors.transferable import IAppSpecificTransfer
from docpool.base.behaviors.transferable import ITransferable
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.testing import DOCPOOL_TRANSFER_FUNCTIONAL_TESTING
from plone import api
from zope.component import getGlobalSiteManager

import unittest


testapp_calls = []


class TestAppSpecificTransfer:
    def __init__(self, original, transfer_folder):
        self.original = original
        self.transfer_folder = transfer_folder

    def assert_allowed(self):
        return True

    def sender_log_entry(self):
        return {}

    def receiver_log_entry(self):
        return {}

    def __call__(self, copy):
        testapp_calls.append((self.original, self.transfer_folder, copy))


class TestTransferFunctional(unittest.TestCase):
    layer = DOCPOOL_TRANSFER_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer["portal"]
        self.source = portal["test_docpool"]
        self.target_dp_a = portal["target_docpool_a"]
        self.target_tf_a = self.target_dp_a["content"]["Transfers"]["from_test"]
        self.target_dp_b = portal["target_docpool_b"]
        self.target_tf_b = self.target_dp_b["content"]["Transfers"]["from_test"]
        testapp_calls.clear()

        getGlobalSiteManager().registerAdapter(
            TestAppSpecificTransfer,
            (IDPDocument, IDPTransferFolder),
            IAppSpecificTransfer,
            "testapp",
        )

    def tearDown(self):
        getGlobalSiteManager().unregisterAdapter(
            None,
            (IDPDocument, IDPTransferFolder),
            IAppSpecificTransfer,
            "testapp",
        )

    def test_transfer_to_multiple_targets_handles_unknown_app(self):
        self.source.supportedApps = ("testapp",)
        self.target_dp_b.supportedApps = ("testapp",)
        document = api.content.create(
            container=self.source["content"]["Groups"]["test_docpool_Members"],
            type="DPDocument",
            id="note",
            title="Note",
            docType="note",
            local_behaviors=["testapp"],
        )
        # Transfer to both targets, pass a (that doesn't have testapp) first on purpose. This is to make sure
        # removal of apps not present at the transfer target affects only the transfer to that target.
        ITransferable(document).transferToTargets([self.target_tf_a.UID(), self.target_tf_b.UID()])
        # sanity check: source document shouldn't have been changed
        self.assertEqual(["testapp"], document.local_behaviors)
        # copy transferred to target that doesn't have testapp should have testapp removed
        self.assertEqual([], self.target_tf_a["note"].local_behaviors)
        # copy transferred to target that does have testapp should have it assigned
        self.assertEqual(["testapp"], self.target_tf_b["note"].local_behaviors)
        # testapp-specific transfer code should have been run exactly for target b
        self.assertEqual([(document, self.target_tf_b, self.target_tf_b["note"])], testapp_calls)
