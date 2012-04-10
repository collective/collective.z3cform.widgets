import zope.interface
import zope.component
import zope.schema
from collective.z3cform.widgets.interfaces import IKeywordsWidget
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.converter import BaseDataConverter
from z3c.form.browser import textarea
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from Acquisition import Explicit

#textarea.TextAreaWidget

class KeywordsWidget(textarea.TextAreaWidget):
    """Input type sequence widget implementation."""
    zope.interface.implementsOnly(IKeywordsWidget)
    klass = u"keyword-widget"
    display_template = ViewPageTemplateFile('keywords_display.pt')
    input_template = ViewPageTemplateFile('keywords_input.pt')
    
    # JavaScript template
    js_template = """\
    (function($) {
        $().ready(function() {
            var newValues = [%(newtags)s]
            var oldValues = [%(oldtags)s]
            $('#%(id)s').data('klass','%(klass)s');
            keywordTokenInputActivate('%(id)s', newValues, oldValues)
            %(js_extra)s
        });
    })(jQuery);
    """
    # def update(self):
    #         pass
    def js_extra(self):
        return ""

    def js(self):
        values = self.context.portal_catalog.uniqueValuesFor('Subject')
        old_values = self.context.Subject()
        tags = ""
        old_tags = ""
        index = 0
        for index, value in enumerate(values):
            tags += "{id: '%s', name: '%s'}" % (value, value)
            if index < len(values) - 1:
                tags += ", "
        old_index = 0
        #import pdb; pdb.set_trace()
        for index, value in enumerate(old_values):
            old_tags += "{id: '%s', name: '%s'}" % (value, value)
            if index < len(old_values) - 1:
                old_tags += ", "

        return self.js_template % dict(id=self.id,
            klass=self.klass,
            newtags=tags,
            oldtags=old_tags,
            js_extra=self.js_extra())

    def render(self):
        if self.mode == interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)

@zope.interface.implementer(interfaces.IFieldWidget)
def KeywordsFieldWidget(field, request):
    """IFieldWidget factory for TextLinesWidget."""
    return widget.FieldWidget(field, KeywordsWidget(request))


@zope.interface.implementer(interfaces.IFieldWidget)
def KeywordsWidgetFactory(field, value_type, request):
    import pdb;pdb.set_trace()
    """IFieldWidget factory for TextLinesWidget."""
    return KeywordsFieldWidget(field, request)



class KeywordsConverter(BaseDataConverter):
    """Data converter for ITextLinesWidget."""

    zope.component.adapts(
        zope.schema.interfaces.ISequence, IKeywordsWidget)

    def toWidgetValue(self, value):
        """Convert from text lines to HTML representation."""
        # if the value is the missing value, then an empty list is produced.
        if value is self.field.missing_value:
            return u''
        return u'\n'.join(unicode(v) for v in value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]
        if not len(value):
            return self.field.missing_value
        valueType = self.field.value_type._type
        #import pdb; pdb.set_trace()
        if isinstance(valueType, tuple):
            valueType = valueType[0]
        return collectionType(valueType(v) for v in value.splitlines())