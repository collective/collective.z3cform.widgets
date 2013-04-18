# -*- coding:utf-8 -*-
import logging

from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore.utils import getToolByName


def upgrade_1_to_2(context, logger=None):
    """
    """
    if logger is None:
        # Called as upgrade step: define our own logger
        logger = logging.getLogger('collective.z3cform.widgets')

    profile = 'profile-collective.z3cform.widgets:1_to_2'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)


def trim_subjects(context, logger=None):
    """Grab all Dexterity content types and trim their related Sujects field.
    """
    if context is not None:
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IDexterityContent.__identifier__)
        for item in results:
            keywords = item.Subject  # a brain has all the information we need
            if keywords:  # our object has keywords; let's trim them
                trimmed_keywords = tuple([k.strip() for k in keywords])
                if trimmed_keywords != keywords:
                    # we reindex only if at least one keyword was changed
                    obj = item.getObject()
                    obj.subject = trimmed_keywords
                    obj.reindexObject(idxs=['Subjects'])
