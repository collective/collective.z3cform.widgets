# -*- coding: utf-8 -*-

from collective.z3cform.widgets.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest2 as unittest

PROJECTNAME = 'collective.z3cform.widgets'
JAVASCRIPTS = [
    '++resource++collective.z3cform.widgets/related.js',
    '++resource++collective.z3cform.widgets/jquery.tokeninput.min.js',
    '++resource++collective.z3cform.widgets/keywords.js',
    '++resource++plone.formwidget.contenttree/contenttree.js',
]

CSS = [
    '++resource++collective.z3cform.widgets/related.css',
    '++resource++collective.z3cform.widgets/token-input-facebook.css',
    '++resource++plone.formwidget.contenttree/contenttree.css',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_jsregistry(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JAVASCRIPTS:
            self.assertIn(js, portal_javascripts.getResourceIds(),
                          '%s not installed' % js)

    def test_cssregistry(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.assertIn(
                css, portal_css.getResourceIds(), '%s not installed' % css)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_jsregistry_removed(self):
        portal_javascripts = self.portal.portal_javascripts
        for js in JAVASCRIPTS:
            self.assertNotIn(js, portal_javascripts.getResourceIds(),
                             '%s not removed' % js)

    def test_cssregistry_removed(self):
        portal_css = self.portal.portal_css
        for css in CSS:
            self.assertNotIn(
                css, portal_css.getResourceIds(), '%s not removed' % css)
