Django Test Runner plugin for Kiwi TCMS
=======================================

.. image:: https://tidelift.com/badges/package/pypi/kiwitcms-django-plugin
    :target: https://tidelift.com/subscription/pkg/kiwitcms-django-plugin?utm_source=pypi-kiwitcms-django-plugin&utm_medium=github&utm_campaign=readme
    :alt: Tidelift

.. image:: https://img.shields.io/twitter/follow/KiwiTCMS.svg
    :target: https://twitter.com/KiwiTCMS
    :alt: Kiwi TCMS on Twitter


This package provides a Django test runner that reports the test results to
`Kiwi TCMS <https://kiwitcms.org>`_.


Installation
------------

::

    pip install kiwitcms-django-plugin


Configuration and environment
-----------------------------


Minimal config file ``~/.tcms.conf``::

    [tcms]
    url = https://tcms.server/xml-rpc/
    username = your-username
    password = your-password

For more info see `tcms-api docs <https://tcms-api.readthedocs.io>`_.

Usage
-----

In ``settings.py`` add the following::

    TEST_RUNNER = 'tcms_django_plugin.TestRunner'

When you run ``./manage.py test`` Django looks at the ``TEST_RUNNER`` setting
to determine what to do.


Changelog
---------

v12.7 (10 Dec 2023)
~~~~~~~~~~~~~~~~~~~

- Update tcms-api from 11.4 to 12.7
- Build & test with Python 3.11
- Refactor issues found by newer pylint
- Refactor issues found by CodeQL
- Reformat source code with Black


v11.3 (15 Jul 2022)
~~~~~~~~~~~~~~~~~~~

- Update tcms-api from 11.2 to 11.4
- Small linter updates


v11.2 (16 May 2022)
~~~~~~~~~~~~~~~~~~~

- Update tcms-api from 11.0 to 11.2
- Annotate plugin with name & version information


v11.1 (05 Dec 2021)
~~~~~~~~~~~~~~~~~~~

- Forward compatible with upcoming Kiwi TCMS v11.0
- Update tcms-api from 10.0 to 11.0
- Use f-strings
- Updates in testing environments


v10.0 (02 Mar 2021)
~~~~~~~~~~~~~~~~~~~

- Compatible with Kiwi TCMS v10.0
- Update tcms-api to 10.0


v9.0 (13 Jan 2021)
~~~~~~~~~~~~~~~~~~

- Compatible with Kiwi TCMS v9.0
- Update to tcms-api v9.0
- Specify valid DJANGO_SETTINGS_MODULE for running pylint-django in CI


v1.1.3 (28 October 2020)
~~~~~~~~~~~~~~~~~~~~~~~~

- Update to tcms-api v8.6.0


v1.1.2 (25 June 2020)
~~~~~~~~~~~~~~~~~~~~~

- Update to tcms-api v8.4.0


v1.1.1 (25 June 2020)
~~~~~~~~~~~~~~~~~~~~~

- Initial release, thanks to Bryan Mutai
