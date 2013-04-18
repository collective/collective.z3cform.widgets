# -*- coding: utf-8 -*-

from collective.z3cform.widgets.testing import FUNCTIONAL_TESTING
from plone.testing import layered

import robotsuite
import unittest

import pkg_resources
PLONE_VERSION = pkg_resources.require("Plone")[0].version

tests = [
    'test_token_input_strip.txt',
]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite(t), layer=FUNCTIONAL_TESTING)
        for t in tests
    ])
    return suite
