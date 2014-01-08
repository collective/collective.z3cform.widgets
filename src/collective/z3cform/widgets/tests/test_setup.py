# -*- coding: utf-8 -*-

from collective.z3cform.widgets.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers

import unittest

PROJECTNAME = 'collective.z3cform.widgets'
EXPECTED_JS = (
    '++resource++collective.z3cform.widgets/related.js',
    '++resource++collective.z3cform.widgets/waypoints.min.js',
    '++resource++collective.z3cform.widgets/jquery.tokeninput.min.js',
    '++resource++collective.z3cform.widgets/keywords.js',
    '++resource++collective.z3cform.widgets/jquery.tasksplease.js',
    '++resource++collective.z3cform.widgets/jquery.rte.js',
)

EXPECTED_CSS = (
    '++resource++collective.z3cform.widgets/related.css',
    '++resource++collective.z3cform.widgets/token-input-facebook.css',
    '++resource++collective.z3cform.widgets/rte.css',
)


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_is_registered(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('ILayer', layers)

    def test_js_are_registered(self):
        actual_js = self.portal.portal_javascripts.getResourceIds()
        for id in EXPECTED_JS:
            self.assertIn(id, actual_js)

    def test_css_are_registered(self):
        actual_css = self.portal.portal_css.getResourceIds()
        for id in EXPECTED_CSS:
            self.assertIn(id, actual_css)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_is_unregistered(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('ILayer', layers)

    def test_js_are_unregistered(self):
        actual_js = self.portal.portal_javascripts.getResourceIds()
        for id in EXPECTED_JS:
            self.assertNotIn(id, actual_js)

    def test_css_are_unregistered(self):
        actual_css = self.portal.portal_css.getResourceIds()
        for id in EXPECTED_CSS:
            self.assertNotIn(id, actual_css)
