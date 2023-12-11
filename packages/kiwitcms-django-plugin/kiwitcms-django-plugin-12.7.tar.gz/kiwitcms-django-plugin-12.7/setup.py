#!/usr/bin/env python
import os
from setuptools import setup


def get_version():
    version_py_path = os.path.join("tcms_django_plugin", "version.py")
    with open(version_py_path, encoding="utf-8") as version_file:
        version = version_file.read()
        return (
            version.replace(" ", "")
            .replace("__version__=", "")
            .strip()
            .strip("'")
            .strip('"')
        )


with open("README.rst", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()

with open("requirements.txt", encoding="utf-8") as file:
    REQUIREMENTS = file.readlines()

setup(
    name="kiwitcms-django-plugin",
    version=get_version(),
    packages=["tcms_django_plugin"],
    description="Django test runner plugin for Kiwi TCMS",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    author="Bryan Mutai",
    author_email="work@bryanmutai.co",
    maintainer="Kiwi TCMS",
    maintainer_email="info@kiwitcms.org",
    license="GPLv3",
    url="https://github.com/kiwitcms/django-plugin",
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
