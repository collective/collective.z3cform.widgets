There's a frood who really knows where his towel is
---------------------------------------------------

1.0b11 (2014-11-27)
^^^^^^^^^^^^^^^^^^^

- Rename ``formwidget_autocomplete_new_value`` function in
  ``related.js`` to ``related_widget_new_value``. Has been just copied from
  ``plone.formwidget.autocomplete``.
  [rnixx]

- remove zope.i18n from package dependencies in order to avoid 
  conflicting zcml with between zope.i18n and Zope2 Publihser 
  i18n.zcml
  [jensens]

- Fix package dependencies.
  [hvelarde]


1.0b10 (2014-10-08)
^^^^^^^^^^^^^^^^^^^

- Remove dependency on unittest2 (test run under Python 2.7 only).
  [hvelarde]

- Remove dependency on Pillow. [hvelarde]

- Drop support for Plone 4.1. [hvelarde]

- Install plone.formwidget.contenttree resources to avoid duplication of
  related items field (fixes `#69 in collective.nitf`_). [jpgimenez]

- Make TokenInputFieldWidget be case-insensitive when suggesting Keywords
  [pbauer]


1.0b9 (2013-05-02)
^^^^^^^^^^^^^^^^^^

- Fixed problem Multicontent (type checkbox gets set to radio). [Kosi81]


1.0b8 (2013-04-24)
^^^^^^^^^^^^^^^^^^

- Rename upgrade step profile. Never, ever name a profile with a number as
  first character and never, ever work for 3 weeks in a row. [hvelarde]


1.0b7 (2013-04-19)
^^^^^^^^^^^^^^^^^^

- Refactor JSON view to access the catalog only when there's a query and limit
  the number of tokens returned to 10 (fixes `#32`_). [hvelarde]

- TokenInputFieldWidget now use ajax to bring the subjects. [flecox]

- Refactor method used in upgrade step to increase its performance: we
  recatalog only offending objects and update only the Subjects index.
  [hvelarde]

- Trim Subjects in TokenInputFieldWidget; an upgrade step for updating all
  offending objects in the catalog is included (fixes `#33`_). [flecox]

- Fixed IE8 problem with 2 simultantious checked radio buttons. [Kosi81]


1.0b6 (2013-04-09)
^^^^^^^^^^^^^^^^^^

- Update package documentation. [hvelarde, jpgimenez]

- TokenInputFieldWidget now replaces subjects widget for any Dexterity-based
  content types on the site, but only if the package is installed. [jpgimenez]

- Tested for compatibility with Dexterity 2.0 and Plone 4.3. [hvelarde]

- Plone 4.1 is no longer supported (closes `#25`_). [hvelarde]

1.0b5 (2013-03-25)
^^^^^^^^^^^^^^^^^^

- Remove dependency on zope.i18n as it is causing ConfigurationConflictError
  (issue `#28`_).
  [hvelarde]


1.0b4 (2013-03-23)
^^^^^^^^^^^^^^^^^^

- Fix package dependencies to be Plone 4.3 compatible. [hvelarde]

- Fix the rendered URLs of related items in the MultiContentSearchWidget in
  display_mode to be actual URLs, not the physical path inside Zope.
  [leorochael]


1.0b3 (2013-01-14)
^^^^^^^^^^^^^^^^^^

- Refactoring of the SimpleRichTextWidget to make it work in an AJAX call.
  [quimera]

- Do not mix unicode and strings in TokenInputWiget editing (fixes `#20`_).
  [jsbueno]

- Checking if contenttree js code should be run or not. [Flecox]

- Test compatibility with Plone 4.3. [hvelarde]

- Add Pillow as a dependency of the package. [hvelarde]

- Import ViewPageTemplateFile from zope.browserpage to avoid dependency on
  zope.app.pagetemplate.
  [hvelarde]


1.0b2 (2012-09-27)
^^^^^^^^^^^^^^^^^^

- New field and widget included which uses the rte-light editor [frapell]


1.0b1 (2012-09-16)
^^^^^^^^^^^^^^^^^^

- Added Dutch translation. [kingel]

- Correction in tasks layout. [quimera]

- Spinners for the related widget so you know is working. [frapell]


1.0a4 (2012-09-04)
^^^^^^^^^^^^^^^^^^

- Spanish translation was updated; Brazilian Portuguese translation was
  added. [hvelarde]

- Resources are only loaded for logged in users. [quimera]

- Ordered search catalog in MultiContentSearchFieldWidget. [flecox]

- Infinite Scroll in MultiContentSearchFieldWidget (fixes `#10`_). [flecox]

- Fix bug when searching with no results in MultiContentSearchFieldWidget.
  [flecox]

- Updating taskplease library in EnhancedTextLinesFieldWidget (fixes `#13`_).
  [flecox]


1.0a3 (2012-06-15)
^^^^^^^^^^^^^^^^^^

- Updated package documentation. [hvelarde]

- Fixing style in EnhancedTextLinesFieldWidget and TokenInputFieldWidget.
  [flecox]

- TasksWidget was renamed to EnhancedTextLinesFieldWidget (fixes `#7`_).
  [hvelarde]

- Changing the name of RelatedContentWidget to MultiContentSearchFieldWidget.
  [flecox]


1.0a2 (2012-05-18)
^^^^^^^^^^^^^^^^^^

- Updated package documentation. [hvelarde]

- Changing the name of KeywordWidget to a better name TokenInputFieldWidget.
  [flecox]

- Now you can add a token just by pressing Enter. [flecox]


1.0a1 (2012-05-04)
^^^^^^^^^^^^^^^^^^

- Initial release.

.. _`#7`: https://github.com/collective/collective.z3cform.widgets/issues/7
.. _`#10`: https://github.com/collective/collective.z3cform.widgets/issues/10
.. _`#13`: https://github.com/collective/collective.z3cform.widgets/issues/13
.. _`#20`: https://github.com/collective/collective.z3cform.widgets/issues/20
.. _`#25`: https://github.com/collective/collective.z3cform.widgets/issues/25
.. _`#28`: https://github.com/collective/collective.z3cform.widgets/issues/28
.. _`#32`: https://github.com/collective/collective.z3cform.widgets/issues/32
.. _`#33`: https://github.com/collective/collective.z3cform.widgets/issues/33
.. _`#69 in collective.nitf`: https://github.com/collective/collective.nitf/issues/69
