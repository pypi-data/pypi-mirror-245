Instrumenting
=============

install
-------

-  install with your favorite Python package manager

.. code:: sh

   pip3 install shopcloud-django-instrumenting

LogRequestMiddleware
~~~~~~~~~~~~~~~~~~~~

add additional Information from request in AppEngine to Log

usage
^^^^^

add to MIDDLEWARE in django-app settings.py:

.. code:: python

   MIDDLEWARE = [
       ...
       'shopcloud_django_instrumenting.middleware.LogRequestMiddleware',
   ]

tracing
-------

.. code:: py

   from shopcloud_django_instrumenting import tracing

   tr = tracing.Tracer('name_of_service', 'name_of_operation')
   with tr.start_span('event.processing') as span:
       pass

   data = tr.close()

deploy
------

.. code:: sh

   $ rm -rf build dist
   $ pip3 install wheel twine
   $ python3 setup.py sdist bdist_wheel
   $ twine upload dist/*

develop
-------

.. code:: sh

   $ pytest
   $ pip3 install coverage
   # shell report
   $ coverage run -m pytest  && coverage report --show-missing
   # html report
   $ coverage run -m pytest  && coverage html
   $ cd htmlcov
   $ python3 -m http.server
