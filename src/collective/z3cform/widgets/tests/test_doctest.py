# -*- coding: utf-8 -*-

from collective.z3cform.widgets.testing import FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest2 as unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/functional.txt',
                                     package='collective.z3cform.widgets'),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
