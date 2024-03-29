##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.onlinehelp package

"""
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(name='zope.app.onlinehelp',
      version='5.1.dev0',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Framework for Context-Sensitive Help Pages',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      keywords="zope3 online help",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      url='http://github.com/zopefoundation/zope.app.onlinehelp',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      python_requires='>=3.7',
      install_requires=[
          'persistent',
          'setuptools',
          'zope.app.component',
          'zope.app.file >= 4.0.0',
          'zope.app.pagetemplate >= 4.0.0',
          'zope.app.publication >= 4.2.1',
          'zope.app.security >= 4.0.0',
          'zope.component',
          'zope.configuration',
          'zope.container',
          'zope.contenttype',
          'zope.i18n',
          'zope.interface',
          'zope.location',
          'zope.publisher >= 4.3.1',
          'zope.schema',
          'zope.security >= 4.1.1',
          'zope.testing',
          'zope.traversing',
      ],
      extras_require={
          'test': [
              'webtest',
              'zope.app.basicskin >= 4.0.0',
              'zope.app.folder',
              'zope.app.http',
              'zope.app.authentication >= 4.0.0',
              'zope.app.principalannotation',
              'zope.app.preference >= 4.0.0',
              'zope.app.renderer >= 4.0.0',
              'zope.app.rotterdam >= 4.0.0',
              'zope.app.wsgi',
              'zope.annotation',
              'zope.copypastemove',
              'zope.configuration',
              'zope.formlib',
              'zope.login',
              'zope.principalannotation',
              'zope.securitypolicy',
              'zope.site',
              'zope.testing',
              'zope.testrunner',
          ],
          'docs': [
              'Sphinx',
              'repoze.sphinx.autointerface',
              'sphinx_rtd_theme',
          ]
      },
      include_package_data=True,
      zip_safe=False,
      )
