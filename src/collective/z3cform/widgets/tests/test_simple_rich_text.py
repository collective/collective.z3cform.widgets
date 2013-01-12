# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName


from collective.z3cform.widgets.testing import INTEGRATION_TESTING


class WidgetTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_configuration(self):
        from collective.z3cform.widgets.simple_rich_text import \
            SimpleRichTextWidget, SimpleRichText
        portal = self.portal
        ttool = getToolByName(self.portal, 'portal_types')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = ttool.getTypeInfo("Document")
        obj = fti.constructInstance(portal, "test1")

        mock_request = object()
        widget = SimpleRichTextWidget(mock_request)
        widget.context = obj
        widget.id = 'test'
        widget.field = SimpleRichText()

        result = widget.rte_conf()
        conf = {
            'iframe_height': 100,
            'format_block': 'true',
            'bold': 'true',
            'italic': 'true',
            'unordered_list': 'true',
            'link': 'true',
            'image': 'true',
            'allow_disable': 'true'
        }

        self.assertEqual(result, conf)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
