# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '1.0b5'
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.z3cform.widgets',
      version=version,
      description="A widget package for Dexterity projects.",
      long_description=long_description,
      classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Framework :: Plone",
            "Framework :: Plone :: 4.1",
            "Framework :: Plone :: 4.2",
            "Framework :: Plone :: 4.3",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
            "Operating System :: OS Independent",
            "Programming Language :: JavaScript",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Topic :: Office/Business :: News/Diary",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: User Interfaces",
      ],
      keywords='plone z3cform widgets dexterity',
      author='Gonzalo Almeida',
      author_email='flecox@ravvit.net',
      url='https://github.com/collective/collective.z3cform.widgets',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.z3cform'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.js.jqueryui',
          'Pillow',
          'plone.app.dexterity>=1.2.1',
          'plone.app.layout',
          'plone.app.vocabularies',
          'plone.formwidget.autocomplete>=1.2.0',
          'plone.formwidget.contenttree',
          'Products.CMFCore',
          'Products.CMFPlone>=4.1',
          'Products.GenericSetup',
          'setuptools',
          'z3c.form',
          'zope.browserpage',
          'zope.component',
          #'zope.i18n',  # FIXME: https://github.com/collective/collective.z3cform.widgets/issues/28
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.i18n',
              'plone.testing',
              'plone.z3cform>=0.7.4',
              'unittest2',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
