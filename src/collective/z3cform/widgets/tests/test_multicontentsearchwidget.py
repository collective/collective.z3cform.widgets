# -*- coding: utf-8 -*-

from collective.z3cform.widgets.multicontent_search_widget import MultiContentSearchWidget
from collective.z3cform.widgets.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.formwidget.contenttree import PathSourceBinder
from zope.component import getMultiAdapter
from zope.schema import Choice
from zope.schema import List

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

    def test_js(self):
        widget = MultiContentSearchWidget(self.request)
        widget.context = self.obj
        widget.name = 'test'
        widget.field = List(value_type=Choice(title=u"Selection",
                                              source=PathSourceBinder(portal_type='Document')))

        result = widget.js_extra()
        self.assertIn('$(\'#test-widgets-query\').each(function()', result)

    def test_render(self):
        view = getMultiAdapter((self.portal, self.request), name='test-collective-z3cform-widgets')

        result = view()
        self.assertIn('++widget++form.widgets.friends/@@autocomplete-search', result)
