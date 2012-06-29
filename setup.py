#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()
execfile(os.path.join(os.path.dirname(__file__), 'markdownify', 'version.py'))


setup(
    name='markdownify',
    description='Convert HTML to markdown.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    version=__version__,
    author='Matthew Tretter',
    author_email='matthew@exanimo.com',
    url='http://github.com/matthewwithanm/markdownify',
    download_url='http://github.com/matthewwithanm/markdownify/tarball/master',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    tests_require=[
        'nose',
        'unittest2',
    ],
    install_requires=[
        'lxml',
        'BeautifulSoup',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ],
    setup_requires=[],
    test_suite='runtests.collector',
)
