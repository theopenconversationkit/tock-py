import os
import re

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

PKG = "tock"
VERSIONFILE = os.path.join(PKG, "__version__.py")

try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass  # Okay, there is no version file.
else:
    VSRE = r"^verstr = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        version = mo.group(1)
    else:
        print("unable to find version in %s" % (VERSIONFILE,))
        raise RuntimeError("if %s.py exists, it is required to be well-formed" % (VERSIONFILE,))

setuptools.setup(
    name="tock-py",
    version=version,
    author="Erwan LE BESCOND",
    author_email="elebescond@gmail.com",
    description="Build chatbots using Tock and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theopenconversationkit/tock-py/",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp==3.6.2',
        'asyncio==3.4.3',
        'marshmallow==3.7.1',
        'marshmallow_enum==1.5.1',
        'marshmallow-oneofschema==2.0.1',
        'testfixtures==6.14.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
