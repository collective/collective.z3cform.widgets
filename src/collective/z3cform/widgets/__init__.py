# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.z3cform.widgets')

from plone.autoform.interfaces import WIDGETS_KEY
from plone.directives.form.schema import TEMP_KEY
from plone.app.dexterity.behaviors.metadata import ICategorization
from zope import schema as _schema

_directives_values = ICategorization.queryTaggedValue(TEMP_KEY)
_directives_values.setdefault(WIDGETS_KEY, {})
_directives_values[WIDGETS_KEY]['subjects'] = 'collective.z3cform.widgets.keywords_widget.KeywordsFieldWidget'
_schema.getFields(ICategorization)['subjects'].index_name = 'Subject'