# -*- coding: utf-8 -*-

from collective.z3cform.widgets.interfaces import ILayer
from collective.z3cform.widgets.testing import INTEGRATION_TESTING
from collective.z3cform.widgets.token_input_widget import TokenInputWidget
from collective.z3cform.widgets.upgrades import trim_subjects
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import unittest


class TokenInputWidgetTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        alsoProvides(self.request, ILayer)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        types = self.portal['portal_types']
        fti = types.getTypeInfo('dexteritytest')
        self.obj = fti.constructInstance(self.portal, 'test1')

    def test_token_input_widget_unicode(self):
        # see: https://github.com/collective/collective.z3cform.widgets/issues/20

        class MockCatalog(object):
            def uniqueValuesFor(self, *args):
                return ["maçã"]

        self.obj.portal_catalog = MockCatalog()
        self.obj.Subject = lambda: ["resumé"]

        widget = TokenInputWidget(self.request)
        widget.context = self.obj

        result = widget.js()

        self.assertTrue(isinstance(result, unicode))
        self.assertTrue(u"resumé" in result)

    def test_token_input_widget_subjects(self):

        class MockCatalog(object):
            def uniqueValuesFor(self, *args):
                return ["maçã", "foo"]

        self.obj.portal_catalog = MockCatalog()
        self.obj.Subject = lambda: ["resumé", "bar"]

        widget = TokenInputWidget(self.request)
        widget.context = self.obj

        result = widget.js()

        self.assertTrue(isinstance(result, unicode))
        self.assertTrue(u"resumé" in result)
        self.assertTrue(u"bar" in result)

    def test_token_input_widget_trim_subjects(self):
        self.obj.subject = ("   resume  ", "  bar")
        self.obj.reindexObject(idxs=['Subjects'])

        trim_subjects(self.portal)
        self.assertEqual(self.obj.subject, ("resume", "bar"))

    def test_export_subject_json_view(self):
        self.obj.subject = ("resume", "bar")
        self.obj.reindexObject(idxs=['Subjects'])

        view = getMultiAdapter((self.portal, self.request), name="json-subjects")
        self.assertEqual(view(), '[]')

        self.request['q'] = 'bar'
        view = getMultiAdapter((self.portal, self.request), name="json-subjects")
        self.assertEqual(view(), '[{"id": "bar", "name": "bar"}]')
