# -*- coding: utf-8 -*-

import zope.component
import zope.interface
import zope.schema

from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import textarea
from Products.Five.browser import BrowserView
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from collective.z3cform.widgets.interfaces import ITokenInputWidget
from collective.z3cform.widgets.interfaces import ILayer

import json


class ExportSubjectAsJSON(BrowserView):
    """Return JSON search results for jQuery Tokeninput
    for more information, see: http://loopj.com/jquery-tokeninput/#installation--setup
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.request.response.setHeader("Content-type", "application/json")
        if 'q' in self.request.keys():
            query = self.request['q']
            keys = self.context.portal_catalog.uniqueValuesFor('Subject')
            keys = [k for k in keys if query.lower() in k.lower()]
        else:
            keys = []

        # we will return up to 10 tokens only
        tokens = map(self._tokenize, keys[:10])
        return json.dumps(tokens)

    def _tokenize(self, value):
        if isinstance(value, str):
            value = value.decode('utf-8')

        return {'id': '%s' % value.replace(u"'", u"\\'"),
                'name': '%s' % value.replace(u"'", u"\\'")}


class TokenInputWidget(textarea.TextAreaWidget):
    """Widget for adding new keywords and autocomplete with the ones in the
    system."""
    zope.interface.implementsOnly(ITokenInputWidget)
    klass = u"token-input-widget"
    display_template = ViewPageTemplateFile('token_input_display.pt')
    input_template = ViewPageTemplateFile('token_input_input.pt')

    # JavaScript template
    js_template = u"""\
    (function($) {
        $().ready(function() {
            var newValues = '%(newtags)s';
            var oldValues = [%(oldtags)s];
            $('#%(id)s').data('klass','%(klass)s');
            keywordTokenInputActivate('%(id)s', newValues, oldValues);
        });
    })(jQuery);
    """

    def js(self):
        if not ILayer.providedBy(self.request):
            return ""
        old_values = self.context.Subject()
        old_tags = u""
        index = 0
        newtags = self.context.absolute_url() + "/json-subjects"
        # prepopulate
        for index, value in enumerate(old_values):
            if isinstance(value, str):
                value = value.decode("utf-8")
            old_tags += u"{id: '%s', name: '%s'}" % (value.replace(
                u"'", u"\\'"), value.replace(u"'", u"\\'"))
            if index < len(old_values) - 1:
                old_tags += ", "
        result = self.js_template % dict(
            id=self.id,
            klass=self.klass,
            newtags=newtags,
            oldtags=old_tags
        )
        return result

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)


@zope.interface.implementer(interfaces.IFieldWidget)
def TokenInputFieldWidget(field, request):
    """IFieldWidget factory for TokenInputWidget."""
    return widget.FieldWidget(field, TokenInputWidget(request))
