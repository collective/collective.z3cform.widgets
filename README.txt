**************************
collective.z3cform.widgets
**************************

.. contents:: Table of Contents

Overview
--------

A widget package for Plone 4 projects.

collective.z3cform.widgets provides the following widgets:

1) TasksWidget: a widget to add a list of options; this widget will degrade to <textarea> if JavaScript is not enabled. to use this Widget we must use a List field or a Tuple field with the value_type as a schema.TextLine() like this:
::
 
  form.widget(options=TasksFieldWidget)
  options = schema.List(
     title=_(u"Available options"),
     value_type= schema.TextLine(),
     default=[],
     required=True)
  

2) KeywordsWidget: a widget for tag input and autocomplete; a widget that uses jquery-tokenunput. This widget will degrade to <textarea> if JavaScript is not enabled.  to use this Widget we must use a List field or a Tuple field with the value_type as a schema.TextLine() like this:
::
 
  form.widget(options=KeywordsFieldWidget)
  options = schema.List(
     title=_(u"Available options"),
     value_type= schema.TextLine(),
     default=[],
     required=True)

3) RelatedContentWidget: a widget to add a dynamic list of objects.. this works as a widget for related items field so it must be used like this:
::

    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(title=u"Related",
                      source=ObjPathSourceBinder(portal_type='Document')),
        required=False,
        )
    form.widget(relatedItems=RelatedContentFieldWidget)

the parameters passed to the ObjPathSourceBinder class are used to filter the search of elements to relate to.. if none parameter are passed, a tree structure is shown in the widget.

4) Future Widgets:

* a widget to select an option from a list; this widget will degrade to
  <select> if JavaScript is not enabled.

* a widget to select multiple options from a list; this widget will degrade to
  <select> if JavaScript is not enabled.



Normal use of Widgets
---------------------

1) Normal use in a form if we have a new field

::

    subjects = schema.Tuple(
        title = _(u'label_categories', default=u'Categories'),
        description = _(u'help_categories', default=u'Also known as keywords, tags or labels, these help you categorize your content.'),
        value_type = schema.TextLine(),
        required = False,
        missing_value = (),
    )

    form.widget(subjects = KeywordsFieldWidget)

2) override and existing field

in an __init__.py of any intalled product 

::

    from plone.autoform.interfaces import WIDGETS_KEY
    from plone.directives.form.schema import TEMP_KEY
    from plone.app.dexterity.behaviors.metadata import ICategorization
    from zope import schema as _schema

    _directives_values = ICategorization.queryTaggedValue(TEMP_KEY)
    _directives_values.setdefault(WIDGETS_KEY, {})
    _directives_values[WIDGETS_KEY]['subjects'] = 'collective.z3cform.widgets.keywords_widget.KeywordsFieldWidget'
    _schema.getFields(ICategorization)['subjects'].index_name = 'Subject'

here we replace the subject's widget.



Requirements
------------

* jQuery >= 1.4

* `Chosen <http://harvesthq.github.com/chosen/>`_

* `Jquery-tokenunput <http://loopj.com/jquery-tokeninput/>`_

Browsers supported
------------------

All modern browsers should be supported (Mozilla Firefox 3.0+, Google Chrome
7.0+, Apple Safari 4.0+, Opera 10.0+ and Microsoft Internet Explorer 9.0+).

