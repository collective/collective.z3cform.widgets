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

    def test_js(self):
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

        result = widget.rte_js()

        rte_js_init = """\
        $("#%(id)s").rte({
            content_css_url: "++resource++collective.z3cform.widgets/rte.css",
            media_url: "++resource++collective.z3cform.widgets/rte/",
            iframe_height: %(iframe_height)s,
            format_block: %(format_block)s,
            bold: %(bold)s,
            italic: %(italic)s,
            unordered_list: %(unordered_list)s,
            link: %(link)s,
            image: %(image)s,
            allow_disable: %(allow_disable)s
        });
        """

        self.assertEqual(result, rte_js_init % dict(id='test',
                                                    iframe_height=100,
                                                    format_block='true',
                                                    bold='true',
                                                    italic='true',
                                                    unordered_list='true',
                                                    link='true',
                                                    image='true',
                                                    allow_disable='true'))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
