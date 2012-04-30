**************************
collective.z3cform.widgets
**************************

.. contents:: Table of Contents

Overview
--------

A widget package for Plone 4 projects.

collective.z3cform.widgets provides the following widgets:

* `a widget to add a list of options
  <https://github.com/collective/collective.z3cform.widgets/issues/1>`_ ; this
  widget will degrade to <textarea> if JavaScript is not enabled.

* `a widget for tag input and autocomplete
  <https://github.com/collective/collective.z3cform.widgets/issues/2>`_ ; when the product is installed, the subject field's widget will be changed for one that uses query-tokenunput. This
  widget will degrade to <textarea> if JavaScript is not enabled.

* a widget to select an option from a list; this widget will degrade to
  <select> if JavaScript is not enabled.

* a widget to select multiple options from a list; this widget will degrade to
  <select> if JavaScript is not enabled.

* `a widget to add a dynamic list of objects
  <https://github.com/collective/collective.z3cform.widgets/issues/3>`_ ; this
  widget will replace the one in collective.formwidget.relationfield that is
  pretty buggy and will be removed from the face of the earth; we need a
  little more brainstorming here.
  if we pass to the source's field: source=ObjPathSourceBinder().. the widget will show a folder tree, otherwise, if we filter this way: source=ObjPathSourceBinder(portal_type='Document') it will show the list of the search result.


How to use the Widgets
----------------------

1) Normal use in a form if we have a new field

.. code:: Python

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

.. code:: Python

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

