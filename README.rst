**************************
collective.z3cform.widgets
**************************

.. contents:: Table of Contents

Overview
--------

A widget package for Plone 4 projects.

collective.z3cform.widgets will provide the following widgets:

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

Requirements
------------

* jQuery >= 1.4

* `Chosen <http://harvesthq.github.com/chosen/>`_

* `Jquery-tokenunput <http://loopj.com/jquery-tokeninput/>`_

Browsers supported
------------------

All modern browsers should be supported (Mozilla Firefox 3.0+, Google Chrome
7.0+, Apple Safari 4.0+, Opera 10.0+ and Microsoft Internet Explorer 9.0+).

