from setuptools import setup

from fairness_metrics import __version__

setup(
    name='fairness_metrics',
    version=__version__,

    url='https://github.com/kylie-g/fairness_metrics_package.git',
    author='Kylie Griep',
    author_email='kng1834@uncw.edu',

    py_modules=['fairness_metrics'],
)
