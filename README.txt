**************************
collective.z3cform.widgets
**************************

.. contents:: Table of Contents

Overview
--------

A widget package for Dexterity projects.

collective.z3cform.widgets provides the following widgets:

**TasksWidget**
    Adds a list of options; degrades to <textarea> if JavaScript is not
    enabled. To use this widget we must use a List field or a Tuple field with
    the value_type as an schema.TextLine() like this::

        form.widget(options=TasksFieldWidget)
        options = schema.List(
            title=_(u"Available options"),
            value_type= schema.TextLine(),
            default=[],
            required=True,
            )

    This widget uses the `jQuery TaskPlease`_ plugin.

**KeywordsWidget**
    Tokenizing autocomplete text entry; will degrade to <textarea> if
    JavaScript is not enabled. To use this Widget we must use a List field or
    a Tuple field with the value_type as a schema.TextLine() like this::

        form.widget(options=KeywordsFieldWidget)
        options = schema.List(
            title=_(u"Available options"),
            value_type= schema.TextLine(),
            default=[],
            required=True,
            )

    This widget uses the `jQuery Tokeninput`_ plugin.

**RelatedContentWidget**
    A widget to add a dynamic list of objects. this works as a widget for
    related items field so it must be used like this::

        relatedItems = RelationList(
            title=_(u'label_related_items', default=u'Related Items'),
            default=[],
            value_type=RelationChoice(title=u"Related",
                          source=ObjPathSourceBinder(portal_type='Document')),
            required=False,
            )
        form.widget(relatedItems=RelatedContentFieldWidget)

    The parameters passed to the ObjPathSourceBinder class are used to filter
    the search of elements to relate to.. if none parameter are passed, a tree
    structure is shown in the widget.

Use
---

New fields
^^^^^^^^^^

::

    subjects = schema.Tuple(
        title = _(u'label_categories', default=u'Categories'),
        description = _(u'help_categories',
                        default=u"Also known as keywords, tags or labels, "
                                u"these help you categorize your content.'),
        value_type = schema.TextLine(),
        required = False,
        missing_value = (,),
        )
    form.widget(subjects = KeywordsFieldWidget)

Override existing fields
^^^^^^^^^^^^^^^^^^^^^^^^

To override an existing field put the following code in the __init__.py of
your package::

    from plone.autoform.interfaces import WIDGETS_KEY
    from plone.directives.form.schema import TEMP_KEY
    from plone.app.dexterity.behaviors.metadata import ICategorization
    from zope import schema as _schema

    _directives_values = ICategorization.queryTaggedValue(TEMP_KEY)
    _directives_values.setdefault(WIDGETS_KEY, {})
    widget = 'collective.z3cform.widgets.keywords_widget.KeywordsFieldWidget'
    _directives_values[WIDGETS_KEY]['subjects'] = widget
    _schema.getFields(ICategorization)['subjects'].index_name = 'Subject'

Here we replace the subject's widget.

Browsers supported
------------------

All modern browsers should be supported (Mozilla Firefox 3.0+, Google Chrome
7.0+, Apple Safari 4.0+, Opera 10.0+ and Microsoft Internet Explorer 9.0+).

Future widgets
--------------

The following widgets will be available in this package in the near future:

* widget to select an option from a list; this widget will degrade to <select>
  if JavaScript is not enabled.

* widget to select multiple options from a list; this widget will degrade to
  <select> if JavaScript is not enabled.

This widgets will probably use the `Chosen`_ plugin.

.. _`jQuery TaskPlease`: https://github.com/Quimera/tasksplease
.. _`jQuery Tokeninput`: http://loopj.com/jquery-tokeninput/
.. _`Chosen`: http://harvesthq.github.com/chosen/

