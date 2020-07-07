import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tock-py",
    version="0.0.1",
    author="Erwan LE BESCOND",
    author_email="elebescond@gmail.com",
    description="Build chatbots using Tock and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theopenconversationkit/tock-py/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)