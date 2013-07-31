#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


pkgmeta = {}
execfile(os.path.join(os.path.dirname(__file__), 'markdownify', 'pkgmeta.py'),
         pkgmeta)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '-s']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


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
    tests_require=[
        'pytest',
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
    cmdclass={
        'test': PyTest,
    },
)
