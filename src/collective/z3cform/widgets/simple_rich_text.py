
from zope.interface import classImplements

from zope.interface import implementsOnly
from zope.interface import implementer

from zope.schema import Bool
from zope.schema import Int
from zope.schema import Text

from zope.schema.fieldproperty import FieldProperty

from zope.schema.interfaces import IText

from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser.textarea import TextAreaWidget

from collective.z3cform.widgets.interfaces import ISimpleRichTextWidget
from collective.z3cform.widgets import _


class SimpleRichTextWidget(TextAreaWidget):
    """
    A widget that implements the rte-light editor
    http://code.google.com/p/rte-light/
    """

    implementsOnly(ISimpleRichTextWidget)

    klass = u"simple-rich-text-widget"

    def rte_conf(self):
        conf = {}
        conf['iframe_height'] = getattr(self.field, 'iframe_height', 100)
        conf['format_block'] = str(getattr(self.field, 'format_block', True)).lower()
        conf['bold'] = str(getattr(self.field, 'bold', True)).lower()
        conf['italic'] = str(getattr(self.field, 'italic', True)).lower()
        conf['unordered_list'] = str(getattr(self.field, 'unordered_list', True)).lower()
        conf['link'] = str(getattr(self.field, 'link', True)).lower()
        conf['image'] = str(getattr(self.field, 'image', True)).lower()
        conf['allow_disable'] = str(getattr(self.field, 'allow_disable', True)).lower()

        return conf


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
        description=(_("Allow to specify the height of the iframe")),
        required=False,
        default=100,
    )

    format_block = Bool(
        title=_("Format block"),
        description=(_('Show the "format block" drop down.')),
        default=True)

    bold = Bool(
        title=_("Bold"),
        description=(_('Show the bold button.')),
        default=True)

    italic = Bool(
        title=_("Italic"),
        description=(_('Show the italic button.')),
        default=True)

    unordered_list = Bool(
        title=_("Unordered list"),
        description=(_('Show the unordered list button.')),
        default=True)

    link = Bool(
        title=_("Link"),
        description=(_('Show the link button.')),
        default=True)

    image = Bool(
        title=_("Image"),
        description=(_('Show the image button.')),
        default=True)

    allow_disable = Bool(
        title=_("Allow to disable"),
        description=(_('Allow to disable the editor.')),
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
