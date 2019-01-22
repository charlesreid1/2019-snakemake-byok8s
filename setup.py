from setuptools import setup, find_packages
import glob
import os

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

# Note: the _program variable is set in __init__.py.
# it determines the name of the package/final command line tool.
from cli import __version__, _program

setup(name='byok8s',
      version=__version__,
      packages=['cli'],
      test_suite='pytest.collector',
      tests_require=['pytest'],
      description='byok8s command line interface',
      url='https://charlesreid1.github.io/2019-snakemake-byok8s',
      author='@charlesreid1',
      author_email='cmreid@ucdavis.edu',
      license='MIT',
      entry_points="""
      [console_scripts]
      {program} = cli.command:main
      """.format(program = _program),
      install_requires=required,
      include_package_data=True,
      keywords=[],
      zip_safe=False)
