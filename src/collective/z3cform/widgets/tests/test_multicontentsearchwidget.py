# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getMultiAdapter
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName

from collective.z3cform.widgets.multicontent_search_widget import \
    MultiContentSearchWidget
from zope.schema import List, Choice
from plone.formwidget.contenttree import PathSourceBinder

from collective.z3cform.widgets.testing import INTEGRATION_TESTING


class WidgetTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_js(self):
        portal = self.portal
        ttool = getToolByName(self.portal, 'portal_types')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = ttool.getTypeInfo("Document")
        obj = fti.constructInstance(portal, "test1")

        widget = MultiContentSearchWidget(self.request)
        widget.context = obj
        widget.name = 'test'
        widget.field = List(value_type=Choice(title=u"Selection",
                                              source=PathSourceBinder(portal_type='Document')))

        result = widget.js_extra()
        self.assertIn('$(\'#test-widgets-query\').each(function()', result)

    def test_render(self):
        view = getMultiAdapter((self.portal, self.request), name='test-collective-z3cform-widgets')

        result = view()
        self.assertIn('++widget++form.widgets.friends/@@autocomplete-search', result)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
