#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

pkgmeta = {
    '__title__': 'markdownify',
    '__author__': 'Matthew Tretter',
    '__version__': '0.11.6',
}

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

setup(
    name='markdownify',
    description='Convert HTML to markdown.',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    version=pkgmeta['__version__'],
    author=pkgmeta['__author__'],
    author_email='m@tthewwithanm.com',
    url='http://github.com/matthewwithanm/python-markdownify',
    download_url='http://github.com/matthewwithanm/python-markdownify/tarball/master',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'beautifulsoup4>=4.9,<5',
        'six>=1.15,<2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities'
    ],
    entry_points={
        'console_scripts': [
            'markdownify = markdownify.main:main'
        ]
    }
)
