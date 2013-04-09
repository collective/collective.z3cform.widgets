# -*- coding:utf-8 -*-
import logging
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
