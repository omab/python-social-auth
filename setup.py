# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
import sys
import os
from os.path import join, dirname, split
from setuptools import setup


PY3 = os.environ.get('BUILD_VERSION') == '3' or sys.version_info[0] == 3

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
    head, tail = split(path)
    return path_tokens(head) + [tail]


def get_packages():
    exclude_pacakages = ('__pycache__',)
    packages = []
    for path_info in os.walk('social'):
        tokens = path_tokens(path_info[0])
        if tokens[-1] not in exclude_pacakages:
            packages.append('.'.join(tokens))
    return packages


requirements_file, tests_requirements_file = {
    False: ('requirements.txt', 'social/tests/requirements.txt'),
    True: ('requirements-python3.txt', 'social/tests/requirements-python3.txt')
}[PY3]

with open(requirements_file, 'r') as f:
    requirements = f.readlines()

with open(tests_requirements_file, 'r') as f:
    tests_requirements = [line for line in f.readlines() if '@' not in line]

setup(
    name='python-social-auth',
    version=version,
    author='Matias Aguirre',
    author_email='matiasaguirre@gmail.com',
    description='Python social authentication made simple.',
    license='BSD',
    keywords='django, flask, pyramid, webpy, openid, oauth, social auth',
    url='https://github.com/omab/python-social-auth',
    packages=get_packages(),
    long_description=long_description(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3'
    ],
    package_data={
        'social/tests': ['social/tests/*.txt']
    },
    extras_require={
        'django': ['social-auth-app-django'],
        'django-mongoengine': ['social-auth-app-django-mongoengine'],
        'flask': ['social-auth-app-flask', 'social-auth-app-flask-sqlalchemy'],
        'flask-mongoengine': ['social-auth-app-flask-mongoengine'],
        'flask-peewee': ['social-auth-app-flask-peewee'],
        'cherrypy': ['social-auth-app-cherrypy'],
        'pyramid': ['social-auth-app-pyramid'],
        'tornado': ['social-auth-app-tornado'],
        'webpy': ['social-auth-app-webpy']
    },
    include_package_data=True,
    tests_require=tests_requirements,
    test_suite='social.tests',
    zip_safe=False
)
