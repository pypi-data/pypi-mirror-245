#
# setup.py
# ~~~~~~~~
# Author: Mark Spain <Mark.Spain@ey.com>
#
# Description:
# IdentityNow API Tenant Configuration
from setuptools import setup, find_packages

VERSION = "0.0.3"
DESCRIPTION = "IdentityNow REST API Client"
LONG_DESCRIPTION = "Implementation of the IdentityNow REST API in Python"

# Setting up
setup(
    name="idnapi",
    version=VERSION,
    author="Mark Spain",
    author_email="Mark.Spain@ey.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests", "python-dateutil"],
    python_requires='>=3',
    keywords=["python", "sailpoint", "identitynow", "idn"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix"
    ]
)
