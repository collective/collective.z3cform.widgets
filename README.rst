**************************
collective.z3cform.widgets
**************************

.. contents:: Table of Contents

Overview
--------

A widget package for Plone 4 projects.

collective.z3cform.widgets will provide the following widgets:

* a widget to add a list of options; this widget will degrade to <textarea> if
  JavaScript is not enabled.
* a widget to select an option from a list; this widget will degrade to
  <select> if JavaScript is not enabled.
* a widget to select multiple options from a list; this widget will degrade to
  <select> if JavaScript is not enabled.
* a widget to select multiple options from a dynamic list of results; for
  instance, a catalog search; this widget will replace the one in
  collective.formwidget.relationfield that is pretty buggy and will be removed
  from the face of the earth; we need a little more brainstorming here.

Requirements
------------

* jQuery >= 1.4
* Chosen (http://harvesthq.github.com/chosen/)

Browsers supported
------------------

All modern browsers should be supported (Mozilla Firefox 3.0+, Google Chrome
7.0+, Apple Safari 4.0+, Opera 10.0+ and Microsoft Internet Explorer 9.0+).

