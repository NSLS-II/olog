from setuptools import find_packages, setup
import versioneer
import sys


min_version = (3, 7)

if sys.version_info < min_version:
    error = """
databroker does not support Python {0}.{1}.
Python {2}.{3} and above is required. Check your Python version like so:

python3 --version

This may be due to an out-of-date pip. Make sure you have pip >= 9.0.1.
Upgrade pip like so:

pip install --upgrade pip
""".format(*(sys.version_info[:2] + min_version))
    sys.exit(error)

with open('requirements.txt') as f:
    requirements = f.read().split()

setup(
    name='olog',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD (3-clause)",
    author='Brookhaven National Laboratory',
    url="https://github.com/NSLS-II/olog",
    packages=find_packages(),
    python_requires='>={}'.format('.'.join(str(n) for n in min_version)),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
