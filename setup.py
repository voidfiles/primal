from glob import glob
from os.path import splitext, basename
import sys

from setuptools.command.test import test as TestCommand
from setuptools import find_packages, setup


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name='primal',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'pynamodb',
        'class-registry',
        'marshmallow==3.0.0b4',
    ],
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
)
