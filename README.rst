
================================
elasticsearch-curator-serverless
================================

This package contains lambda (serverless) handler for execution `elasticsearch curator <https://github.com/elastic/curator>`_ actions.

Official documentation contains section on `serverless deployment <https://www.elastic.co/blog/serverless-elasticsearch-curator-on-aws-lambda>`_ but the
approach / code has shortcomings which this handler tries to address:

* Handles only deletion of indices while there's `plenty of other actions <https://www.elastic.co/guide/en/elasticsearch/client/curator/current/actions.html>`_.

* Bundles configuration with function code, that means function redeployment
  for every configuration change and separate function code for each
  configuration.


Thanks to this `PR <https://github.com/elastic/curator/pull/1035>`_ it's also possible to implement such a handler in clean and easy way.


Requirements
============

* Python 3.6


How to create deployment package
================================

From source
-----------

Clone this repository and change directory to it

.. code-block:: bash

   $ git clone https://github.com/beezz/elasticsearch-curator-serverless.git
   $ cd elasticsearch-curator-serverless

Generate deployment zip package

.. code-block:: bah

   $ make lambda

If you want to bundle in configuration files, use ``CONFIGS`` variable when
calling ``make lambda``

.. code-block:: bash

   $ CONFIGS=/path/to/configs make lamba

Resulting deployment package is located at

``dist/lambda/lambda.zip``


Configure lambda function
=========================

Handler name

``curator_serverless.handler``


Runtime

``Python 3.6``


Configure curator
------------------

Curator configuration can be bundled in the deployment package or downloaded
when the function is triggered from url. Configuration can be provided as
environmental variables or as part of event or mix.

Environmental variables
~~~~~~~~~~~~~~~~~~~~~~~

:CONFIG_FILE: Path to local, bundled file or url to `curator's configuration file <https://www.elastic.co/guide/en/elasticsearch/client/curator/current/configfile.html>`_

:ACTION_FILE: Path to local, bundled file or url to `curator's action file <https://www.elastic.co/guide/en/elasticsearch/client/curator/current/actionfile.html>`_


Event structure
---------------

.. code-block:: json

   {
     "CONFIG_FILE": "https://s3-eu-west-1.amazonaws.com/curator-configs/config.yml",
     "ACTION_FILE": "https://s3-eu-west-1.amazonaws.com/curator-configs/action.yml"
   }


Testing locally
===============

With python3.6 (`virtual <https://virtualenv.pypa.io/en/stable/installation/>`_) environemnt, install the code.

Clone this repository and change directory to it

.. code-block:: bash

   $ git clone https://github.com/beezz/elasticsearch-curator-serverless.git
   $ cd elasticsearch-curator-serverless
   $ pip install --editable .


Run locally and pass event json via stdin. Example with mixing event and environment configuration.

.. code-block:: json

   $ echo '{"ACTION_FILE": "http://localhost:8000/delete.yml"}' | CONFIG_FILE=configs/config.yml python -m curator_serverless.__init__
