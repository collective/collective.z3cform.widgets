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
    """
        Grab all dexterity content types and trim their related sujects
    """

    if context is not None:
        pc = getToolByName(context, 'portal_catalog')
        querySet = pc(**{'path': '/',
                         'object_provides': IDexterityContent.__identifier__})
        for item in querySet:
            obj = item.getObject()
            old_subject = obj.subject
            subjects = old_subject
            if old_subject:
                subjects = [subject.strip() for subject in old_subject]
            obj.subject = subjects
            obj.reindexObject()
