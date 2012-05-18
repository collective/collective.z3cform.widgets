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
    enabled.

    This widget uses the `jQuery TaskPlease`_ plugin.

**TokenInputWidget**
    TokenInputWidget allows your users to select multiple items from a
    predefined list, using autocompletion as they type to find each item. You
    may have seen a similar type of text entry when filling in the recipients
    field sending messages on `Facebook`_. This widget will degrade to
    <textarea> if JavaScript is not enabled.

    .. image:: https://github.com/collective/collective.z3cform.widgets/raw/master/tokeninputwidget.png
        :align: center
        :height: 110px
        :width: 600px

    This widget uses the `jQuery Tokeninput`_ plugin.

**RelatedContentWidget**
    A widget to add a dynamic list of objects. This works as a widget for
    related items field so it must be used like this.

Future widgets
--------------

The following widgets will be available in this package in the near future:

* widget to select an option from a list; this widget will degrade to <select>
  if JavaScript is not enabled.

* widget to select multiple options from a list; this widget will degrade to
  <select> if JavaScript is not enabled.

This widgets will probably use the `Chosen`_ plugin.

Browsers supported
------------------

All modern browsers should be supported (Mozilla Firefox 3.0+, Google Chrome
7.0+, Apple Safari 4.0+, Opera 10.0+ and Microsoft Internet Explorer 9.0+).

.. _`jQuery TaskPlease`: https://github.com/Quimera/tasksplease
.. _`jQuery Tokeninput`: http://loopj.com/jquery-tokeninput/
.. _`Chosen`: http://harvesthq.github.com/chosen/
.. _`Facebook`: http://www.facebook.com/

