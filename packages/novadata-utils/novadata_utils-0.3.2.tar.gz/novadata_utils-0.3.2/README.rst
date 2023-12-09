novadata utils
==============

Package to facilitate your day to day as a Django developer.

Getting Started
----------------

Follow the step by step below to install and configure the package.

Dependencies
~~~~~~~~~~~~

Depends on the following packages (which will be installed automatically):

- Django
- Django Rest Framework
- Django Advanced Filters
- Django Admin List Filter Dropdown
- Django Object Actions
- Django Import Export
- Django Crum

Installation and Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

   pip install novadata-utils

Settings.py:
~~~~~~~~~~~~

.. code-block:: python

   INSTALLED_APPS = [
      ...
      'advanced_filters',
      'django_admin_listfilter_dropdown',
      'django_object_actions',
      'import_export',
      'novadata_utils',
      'rangefilter',
      'rest_framework',
      ...
   ]

   # After Django middlewares
   MIDDLEWARE += ('crum.CurrentRequestUserMiddleware',)

Main urls.py:
~~~~~~~~~~~~~

.. code-block:: python

   urlpatterns = [
      ...
      path('advanced_filters/', include('advanced_filters.urls')),
      ...
   ]

Features
--------

Access the `docs <https://novadata-utils-docs.readthedocs.io/en/latest/usage.html#installation>`_
to see the features and how to use them.
