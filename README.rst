
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

Usage
=====
