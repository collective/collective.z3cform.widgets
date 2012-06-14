# -*- coding: utf-8 -*-

import zope.component
import zope.interface
import zope.schema

from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from collective.z3cform.widgets.interfaces import IEnhancedTextLinesWidget


class EnhancedTextLinesWidget(textarea.TextAreaWidget):
    """ Widget for adding new keywords and autocomplete with the ones in the
    system.
    """
    zope.interface.implementsOnly(IEnhancedTextLinesWidget)
    klass = u"keyword-widget"
    display_template = ViewPageTemplateFile('enhancedtextlines_display.pt')
    input_template = ViewPageTemplateFile('enhancedtextlines_input.pt')

    # JavaScript template
    js_template = """\
    (function($) {
        $().ready(function() {
        tp_i18n = {
            add:'Add',
            add_task:'Add a task',
            delete_task:'Delete task',
            edit_task:'Edit task'
        }
         $('#%(id)s').tasksplease();
        });
    })(jQuery);
    """

    def js(self):
        return self.js_template % dict(id=self.id)

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)


@zope.interface.implementer(interfaces.IFieldWidget)
def EnhancedTextLinesFieldWidget(field, request):
    """ IFieldWidget factory for EnhancedTextLinesFieldWidget.
    """
    return widget.FieldWidget(field, EnhancedTextLinesWidget(request))
