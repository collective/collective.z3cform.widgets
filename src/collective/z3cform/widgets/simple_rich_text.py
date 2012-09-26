
from zope.interface import classImplements

from zope.interface import implementsOnly
from zope.interface import implementer

from zope.schema import Bool
from zope.schema import Int
from zope.schema import Text

from zope.schema.fieldproperty import FieldProperty

from zope.schema.interfaces import IText

from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import DISPLAY_MODE

from z3c.form.widget import FieldWidget

from z3c.form.browser.textarea import TextAreaWidget

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from collective.z3cform.widgets.interfaces import ISimpleRichTextWidget

from collective.z3cform.widgets import _


class SimpleRichTextWidget(TextAreaWidget):
    """
    A widget that implements the rte-light editor
    http://code.google.com/p/rte-light/
    """

    implementsOnly(ISimpleRichTextWidget)

    klass = u"simple-rich-text-widget"
    # display_template = ViewPageTemplateFile('simple_rich_text_display.pt')
    # input_template = ViewPageTemplateFile('simple_rich_text_input.pt')

    # def render(self):
    #     if self.mode == DISPLAY_MODE:
    #         return self.display_template(self)
    #     else:
    #         return self.input_template(self)
    
    def rte_js(self):

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

        iframe_height = getattr(self.field, 'iframe_height', 100)

        format_block = getattr(self.field, 'format_block', True)
        if format_block:
            format_block = "true"
        else:
            format_block = "false"
        bold = getattr(self.field, 'bold', True)
        if bold:
            bold = "true"
        else:
            bold = "false"
        italic = getattr(self.field, 'italic', True)
        if italic:
            italic = "true"
        else:
            italic = "false"
        unordered_list = getattr(self.field, 'unordered_list', True)
        if unordered_list:
            unordered_list = "true"
        else:
            unordered_list = "false"
        link = getattr(self.field, 'link', True)
        if link:
            link = "true"
        else:
            link = "false"
        image = getattr(self.field, 'image', True)
        if image:
            image = "true"
        else:
            image = "false"
        allow_disable = getattr(self.field, 'allow_disable', True)
        if allow_disable:
            allow_disable = "true"
        else:
            allow_disable = "false"

        result = rte_js_init % dict(id=self.id,
                                    iframe_height=iframe_height, 
                                    format_block=format_block,
                                    bold=bold,
                                    italic=italic,
                                    unordered_list=unordered_list,
                                    link=link,
                                    image=image,
                                    allow_disable=allow_disable)

        return result


@implementer(IFieldWidget)
def SimpleRichTextInputFieldWidget(field, request):
    """
    IFieldWidget factory for SimpleRichTextWidget.
    """

    return FieldWidget(field, SimpleRichTextWidget(request))


class ISimpleRichText(IText):
    """Interface for the Simple Rich Text field"""

    iframe_height = Int(
        title=_("Iframe height"),
        description=(
        _("Allow to specify the height of the iframe")),
        required=False,
        default=100,
        )

    format_block = Bool(
        title=_("Format block"),
        description=(
        _('Show the "format block" drop down.')),
        default=True)

    bold = Bool(
        title=_("Bold"),
        description=(
        _('Show the bold button.')),
        default=True)

    italic = Bool(
        title=_("Italic"),
        description=(
        _('Show the italic button.')),
        default=True)

    unordered_list = Bool(
        title=_("Unordered list"),
        description=(
        _('Show the unordered list button.')),
        default=True)

    link = Bool(
        title=_("Link"),
        description=(
        _('Show the link button.')),
        default=True)

    image = Bool(
        title=_("Image"),
        description=(
        _('Show the image button.')),
        default=True)

    allow_disable = Bool(
        title=_("Allow to disable"),
        description=(
        _('Allow to disable the editor.')),
        default=True)


class SimpleRichText(Text):
    """A text field which provides a simple editor."""

    iframe_height = FieldProperty(ISimpleRichText['iframe_height'])
    format_block = FieldProperty(ISimpleRichText['format_block'])
    bold = FieldProperty(ISimpleRichText['bold'])
    italic = FieldProperty(ISimpleRichText['italic'])
    unordered_list = FieldProperty(ISimpleRichText['unordered_list'])
    link = FieldProperty(ISimpleRichText['link'])
    image = FieldProperty(ISimpleRichText['image'])
    allow_disable = FieldProperty(ISimpleRichText['allow_disable'])

    def __init__(self, 
                 iframe_height=100,
                 format_block=True, 
                 bold=True, 
                 italic=True,
                 unordered_list=True,
                 link=True,
                 image=True,
                 allow_disable=True,
                 **kw):

        self.iframe_height = iframe_height
        self.format_block = format_block
        self.bold = bold
        self.italic = italic
        self.unordered_list = unordered_list
        self.link = link
        self.image = image
        self.allow_disable = allow_disable

        super(SimpleRichText, self).__init__(**kw)

classImplements(SimpleRichText, ISimpleRichText)
