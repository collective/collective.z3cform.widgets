# -*- coding:utf-8 -*-

import os
from setuptools import setup, find_packages

version = '1.0a1'
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='collective.z3cform.widgets',
      version=version,
      description="A widget package for Dexterity projects.",
      long_description=long_description,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Office/Business :: News/Diary",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        ],
      keywords='plone z3c widgets dexterity',
      author='Gonzalo Almeida',
      author_email='flecox@ravvit.net',
      url='https://github.com/collective/collective.z3cform.widgets',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.z3cform'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'collective.js.jqueryui',
        'plone.app.dexterity>=1.2.1',
        'plone.formwidget.autocomplete>=1.2.0',
        'plone.z3cform>=0.7.4',
        'z3c.formwidget.query',
        ],
      extras_require={
        'test': ['plone.app.testing', 'plone.formwidget.contenttree'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
