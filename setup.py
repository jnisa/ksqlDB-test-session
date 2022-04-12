

from setuptools import setup
from setuptools import find_packages


# setup the environment
setup(
    name = 'ksqldb-test-session',
    version = '0.1',
    description = 'Test Stage for the ksqlDB',
    package = find_package(),
    author = 'João Nisa',
    include_package_data = True,
)