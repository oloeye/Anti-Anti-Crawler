# -*- coding: utf-8 -*-
# @Author: Hobo
# @Date:   2017-10-31 15:42:03
# @Last Modified by:   Hobo
# @Last Modified time: 2018-01-02 12:10:53

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='proxy_ip_pool',
    version='0.1.0',
    url='https://github.com/luxux/Anti-reptile',
    license='BSD',
    author='Hobo',
    author_email='Hoboalia@gmail.com',
    description='requests+sqlite3+squid',
    long_description=__doc__,
    install_requires=[
        'gevent',
        'requests',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
    py_modules=['ipool'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
