# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.z3cform.widgets.testing import INTEGRATION_TESTING

JAVASCRIPTS = [
    "++resource++collective.z3cform.widgets/related.js",
    "++resource++collective.z3cform.widgets/jquery.tokeninput.min.js",
    "++resource++collective.z3cform.widgets/keywords.js"
    ]

CSS = [
    "++resource++collective.z3cform.widgets/related.css",
    "++resource++collective.z3cform.widgets/token-input-facebook.css"
    ]

class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled("collective.z3cform.widgets"))

    def test_jsregistry(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JAVASCRIPTS:
            self.assertTrue(js in portal_javascripts.getResourceIds(),
                            '%s not installed' % js)

    def test_cssregistry(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.assertTrue(css in portal_css.getResourceIds(),
                            '%s not installed' % css)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=["collective.z3cform.widgets"])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled("collective.z3cform.widgets"))

    def test_jsregistry_removed(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JAVASCRIPTS:
            self.assertFalse(js in portal_javascripts.getResourceIds(),
                             '%s not removed' % js)

    def test_cssregistry_removed(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.assertFalse(css in portal_css.getResourceIds(),
                            '%s not removed' % css)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
