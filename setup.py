from __future__ import absolute_import

import shlex
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
try:
    from setupext.pip import read_requirements_from_file
except ImportError:
    def read_requirements_from_file(req_name):
        reqs = []
        with open(req_name, 'r') as req_file:
            for line in req_file:
                if '#' in line:
                    line = line[0:line.find('#')]
                line = line.strip()
                if line:
                    reqs.append(line)
        return reqs

from messages import version


with open('README.rst', 'r') as readme:
    long_description = readme.read()


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', 'Arguments passed as-is to tox')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        sys.exit(tox.cmdline(args=shlex.split(self.tox_args or '')))



setup(
    name='messages',
    version=version.__version__,
    license='BSD',
    author='Dave Shawley',
    author_email='daveshawley@gmail.com',
    url='http://github.com/dave-shawley/messages',
    description='Makes sending messages easier',
    long_description=long_description,
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=read_requirements_from_file('requirements.txt'),
    setup_requires=['setupext-pip'],
    tests_require=read_requirements_from_file('dev-requirements.txt'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    cmdclass={'test': Tox},
)
