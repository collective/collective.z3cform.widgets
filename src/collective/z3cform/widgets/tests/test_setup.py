# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName


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

    def test_token_input_widget_unicode(self):
        # Created to check issue 20
        # https://github.com/collective/collective.z3cform.widgets/issues/20
        from collective.z3cform.widgets.token_input_widget import\
            TokenInputWidget
        portal = self.portal
        ttool = getToolByName(self.portal, 'portal_types')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = ttool.getTypeInfo("Document")
        obj = fti.constructInstance(portal, "test1")

        class MockCatalog(object):
            def uniqueValuesFor(self, *args):
                return ["maçã"]

        def mock_subject():
            return ["resumé"]
        obj.portal_catalog = MockCatalog()
        obj.Subject = mock_subject

        mock_request = object()
        widget = TokenInputWidget(mock_request)
        widget.context = obj

        result = widget.js()

        self.assertTrue(isinstance(result, unicode))
        self.assertTrue(u"maçã" in result)
        self.assertTrue(u"resumé" in result)

    def test_token_input_widget_subjects(self):
        from collective.z3cform.widgets.token_input_widget import\
            TokenInputWidget
        portal = self.portal
        ttool = getToolByName(self.portal, 'portal_types')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = ttool.getTypeInfo("Document")
        obj = fti.constructInstance(portal, "test1")

        class MockCatalog(object):
            def uniqueValuesFor(self, *args):
                return ["maçã", "foo"]

        def mock_subject():
            return ["resumé", "bar"]
        obj.portal_catalog = MockCatalog()
        obj.Subject = mock_subject

        mock_request = object()
        widget = TokenInputWidget(mock_request)
        widget.context = obj

        result = widget.js()

        self.assertTrue(isinstance(result, unicode))
        self.assertTrue(u"maçã" in result)
        self.assertTrue(u"resumé" in result)
        self.assertTrue(u"foo" in result)
        self.assertTrue(u"bar" in result)


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
