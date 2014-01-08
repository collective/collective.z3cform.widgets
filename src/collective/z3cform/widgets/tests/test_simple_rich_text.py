# -*- coding: utf-8 -*-

from collective.z3cform.widgets.simple_rich_text import SimpleRichText
from collective.z3cform.widgets.simple_rich_text import SimpleRichTextWidget
from collective.z3cform.widgets.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class WidgetTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        types = self.portal['portal_types']
        fti = types.getTypeInfo('Document')
        self.obj = fti.constructInstance(self.portal, 'test1')

    def test_configuration(self):
        mock_request = object()
        widget = SimpleRichTextWidget(mock_request)
        widget.context = self.obj
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
