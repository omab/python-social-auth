# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
import sys
import os
from os.path import join, dirname, split
from setuptools import setup


PY3 = sys.version_info[0] == 3

version = __import__('social').__version__

LONG_DESCRIPTION = """
Python Social Auth is an easy to setup social authentication/registration
mechanism with support for several frameworks and auth providers.

Crafted using base code from django-social-auth, implements a common interface
to define new authentication providers from third parties. And to bring support
for more frameworks and ORMs.
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION


def path_tokens(path):
    if not path:
        return []
    head, tail = os.path.split(path)
    return path_tokens(head) + [tail]


def get_packages():
    exclude_pacakages = ('__pycache__',)
    packages = []
    for path_info in os.walk('social'):
        tokens = path_tokens(path_info[0])
        if tokens[-1] not in exclude_pacakages:
            packages.append('.'.join(tokens))
    return packages


requires = ['requests>=1.1.0', 'oauthlib>=0.3.8', 'six>=1.2.0']
if PY3:
    requires += ['python3-openid>=3.0.1',
                 'requests-oauthlib>=0.3.0,<0.3.2']
else:
    requires += ['python-openid>=2.2', 'requests-oauthlib>=0.3.0']


setup(name='python-social-auth',
      version=version,
      author='Matias Aguirre',
      author_email='matiasaguirre@gmail.com',
      description='Python social authentication made simple.',
      license='BSD',
      keywords='django, flask, pyramid, webpy, openid, oauth, social auth',
      url='https://github.com/omab/python-social-auth',
      packages=get_packages(),
      #package_data={'social': ['locale/*/LC_MESSAGES/*']},
      long_description=long_description(),
      install_requires=requires,
      classifiers=['Development Status :: 4 - Beta',
                   'Topic :: Internet',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Developers',
                   'Environment :: Web Environment',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3'],
      test_suite='social.tests',
      zip_safe=False)
