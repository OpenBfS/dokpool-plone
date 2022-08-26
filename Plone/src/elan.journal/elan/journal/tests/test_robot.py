from elan.journal.testing import ROBOT_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest


dirname = os.path.dirname(__file__)
files = os.listdir(dirname)
tests = [f for f in files if f.startswith("test_") and f.endswith(".robot")]

# FIXME: Re-enable RobotFramework tests that were disabled since Plone 5
tests = []


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                robotsuite.RobotTestSuite(t, noncritical=["Expected Failure"]),
                layer=ROBOT_TESTING,
            )
            for t in tests
        ]
    )
    return suite
