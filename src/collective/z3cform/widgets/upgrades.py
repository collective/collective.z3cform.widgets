# -*- coding:utf-8 -*-

from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore.utils import getToolByName

import logging


def to2(context, logger=None):
    """
    """
    profile = 'profile-collective.z3cform.widgets:upgrade_1_to_2'
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(profile)


def trim_subjects(context, logger=None):
    """Grab all Dexterity content types and trim their related Sujects field.
    """
    if logger is None:
        logger = logging.getLogger('collective.z3cform.widgets')

    if context is not None:
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IDexterityContent.__identifier__)
        for item in results:
            keywords = item.Subject  # a brain has all the information we need
            if keywords:  # our object has keywords; let's trim them
                trimmed_keywords = tuple([k.strip() for k in keywords])
                if trimmed_keywords != keywords:
                    # we replace and reindex only if at least one keyword was changed
                    obj = item.getObject()
                    logger.debug("Subjects field for object '%s' will be modified" % obj.absolute_url_path())
                    obj.subject = trimmed_keywords
                    logger.debug("Changed from %s to %s" % (obj.subject, trimmed_keywords))
                    obj.reindexObject(idxs=['Subjects'])
                    logger.debug("Object reindexed")


def to3(context, logger=None):
    """Install plone.formwidget.contenttree resources to avoid duplication of
    related items field.
    """
    if logger is None:
        logger = logging.getLogger('collective.z3cform.widgets')

    dependency = 'plone.formwidget.contenttree'
    profile = 'profile-{0}:default'.format(dependency)
    qi = getToolByName(context, 'portal_quickinstaller')
    if not qi.isProductInstalled(dependency):
        setup = getToolByName(context, 'portal_setup')
        setup.runAllImportStepsFromProfile(profile)
        logger.info("{0} was installed.".format(dependency))
    else:
        logger.info("{0} already installed; nothing to do.".format(dependency))
