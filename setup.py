# -*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

version = '1.0'

setup(name='collective.z3cform.widgets',
      version=version,
      description="A widget package for Plone 4 projects.",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
                       open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Plone :: 4.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        ],
      keywords='plone z3c widgets',
      author='Silvestre Huens',
      author_email='s.huens@gmail.com',
      url='https://github.com/collective/collective.z3cform.widgets',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective', 'collective.z3cform'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'z3c.formwidget.query',
        'plone.formwidget.autocomplete >= 1.2.0',
        'plone.z3cform >= 0.7.4',
        ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
