###################################
Rose Of Eterity Legacy Reviews ETL
###################################

ETL that:

- downloads review HTML pages
- parses out data (user name, score, comments, and posted on date)
- cleans data
- saves data as CSV
- loads data into database

Installing requirements
-----------------------

Before you start:

- apps should always be run inside of virtualenvs_
- dependencies are managed with pip_ and pip-tools_. Virtualenvs come with
  pip preinstalled; pip-tools should be installed manually with ``python -m pip
  install pip-tools``.


Running the app
-------------------

Before the first run of the app::

    $ pip-compile --upgrade requirements.in
    $ python -m pip install -r dev-requirements.txt


.. _virtualenvs: https://virtualenv.pypa.io/
.. _pip: https://pip.pypa.io/
.. _pip-tools: https://github.com/nvie/pip-tools/