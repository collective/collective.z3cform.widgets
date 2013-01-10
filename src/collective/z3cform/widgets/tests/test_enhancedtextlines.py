# -*- coding: utf-8 -*-

import unittest2 as unittest

from z3c.form.interfaces import DISPLAY_MODE
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.CMFCore.utils import getToolByName

from collective.z3cform.widgets.enhancedtextlines import \
    EnhancedTextLinesWidget

from collective.z3cform.widgets.testing import INTEGRATION_TESTING


class WidgetTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_js(self):
        portal = self.portal
        ttool = getToolByName(self.portal, 'portal_types')
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        fti = ttool.getTypeInfo("Document")
        obj = fti.constructInstance(portal, "test1")

        widget = EnhancedTextLinesWidget(self.portal.REQUEST)
        widget.context = obj
        widget.id = 'test'

        result = widget.js()

        js_template = """\
    (function($) {
        $().ready(function() {
        tp_i18n = {
            add:'%(add)s',
            add_task:'%(add_task)s',
            delete_task:'%(delete_task)s',
            edit_task:'%(edit_task)s'
        }
         $('#%(id)s').tasksplease();
        });
    })(jQuery);
    """

        self.assertEqual(result, js_template % dict(id='test',
                                                    add='Add',
                                                    add_task='Add Option',
                                                    delete_task='Delete Option',
                                                    edit_task='Edit Option'))

        widget_template = """\

<script type="text/javascript">    (function($) {
        $().ready(function() {
        tp_i18n = {
            add:'%(add)s',
            add_task:'%(add_task)s',
            delete_task:'%(delete_task)s',
            edit_task:'%(edit_task)s'
        }
         $('#%(id)s').tasksplease();
        });
    })(jQuery);
    </script>
<textarea id="test" class="keyword-widget"></textarea>

"""

        result = widget.render()
        self.assertEqual(result, widget_template % dict(id='test',
                                                        add='Add',
                                                        add_task='Add Option',
                                                        delete_task='Delete Option',
                                                        edit_task='Edit Option'))

        widget.mode = DISPLAY_MODE
        result = widget.render()
        self.assertEqual(result, u'\n<span id="test" class="keyword-widget"></span>\n\n')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
