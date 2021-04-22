#/usr/bin/env python
import codecs
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand, Command


read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()

pkgmeta = {
    '__title__': 'markdownify',
    '__author__': 'Matthew Tretter',
    '__version__': '0.7.0',
}


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '-s']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


class LintCommand(Command):
    """
    A copy of flake8's Flake8Command

    """
    description = "Run flake8 on modules registered in setuptools"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def distribution_files(self):
        if self.distribution.packages:
            for package in self.distribution.packages:
                yield package.replace(".", os.path.sep)

        if self.distribution.py_modules:
            for filename in self.distribution.py_modules:
                yield "%s.py" % filename

    def run(self):
        from flake8.api.legacy import get_style_guide
        flake8_style = get_style_guide(config_file='setup.cfg')
        paths = self.distribution_files()
        report = flake8_style.check_files(paths)
        raise SystemExit(report.total_errors > 0)


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
    setup_requires=[
        'flake8>=3.8,<4',
    ],
    tests_require=[
        'pytest>=6.2,<7',
    ],
    install_requires=[
        'beautifulsoup4>=4.9,<5', 'six>=1.15,<2'
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
    cmdclass={
        'test': PyTest,
        'lint': LintCommand,
    },
)
