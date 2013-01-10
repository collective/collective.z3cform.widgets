from zope.component import adapts
from zope.interface import Interface, implements
from zope import schema

from plone.z3cform import layout

from z3c.form import form, button, field

from collective.z3cform.widgets.multicontent_search_widget import MultiContentSearchFieldWidget
from plone.formwidget.contenttree import PathSourceBinder


class ITestForm(Interface):

    friends = schema.List(
        title=u"Friend objects",
        description=u"Select as many as you want",
        value_type=schema.Choice(
            title=u"Selection",
            source=PathSourceBinder(portal_type='Document')))


class TestAdapter(object):
    implements(ITestForm)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def _get_friends(self):
        return []

    def _set_friends(self, value):
        print "setting", value
    friends = property(_get_friends, _set_friends)


class TestForm(form.Form):
    fields = field.Fields(ITestForm)
    fields['friends'].widgetFactory = MultiContentSearchFieldWidget

    @button.buttonAndHandler(u'Ok')
    def handle_ok(self, action):
        data, errors = self.extractData()
        print data, errors


TestView = layout.wrap_form(TestForm)
