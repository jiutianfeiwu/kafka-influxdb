Kafka-InfluxDB
==============

|PyPi Version| |Build Status| |Coverage Status| |Code Climate| |Downloads| |Python Versions|

| A Kafka consumer for InfluxDB written in Python.
| All messages sent to Kafka on a certain topic will be relayed to Influxdb.
| Supports InfluxDB 0.9.x. For InfluxDB 0.8.x support, check out the `0.3.0 tag <https://github.com/mre/kafka-influxdb/tree/v0.3.0>`__.
| Supports cluster

Use cases
---------

Kafka will serve as a buffer for your metric data during high load.
Also it's useful for metrics from offshore data centers with unreliable connections to your monitoring backend.

.. figure:: https://raw.githubusercontent.com/mre/kafka-influxdb/master/assets/schema-small.png
   :alt: Usage example


Quickstart
----------

To run the tool from your local machine:

::

    pip install kafka_influxdb
    kafka_influxdb -c config-example.yaml


Benchmark
---------

To see the tool in action, you can start a complete
``CollectD -> Kafka -> kafka_influxdb -> Influxdb`` setup with the
following command:

::

    docker-compose up

This will immediately start reading messages from Kafka and write them
into InfluxDB. To see the output, you can use the InfluxDB Admin Interface.
Check on which port it is running with ``docker ps | grep tutum/influxdb``.
There should be a mapping like 32785->8083/tcp or so.
In this case 32785 is the port where you can reach it.
Then go to ``http://<docker_host_ip>:<port>`` and type ``SHOW MEASUREMENTS``
to see the output. (``<docker_host_ip>`` is probably ``localhost`` on Linux.
On Mac you can find out with ``boot2docker ip`` or ``docker-machine ip``).

By default this will write 1.000.000 sample messages into the
``benchmark`` Kafka topic. After that it will consume the messages again
to measure the throughput. Sample output using the above Docker setup
inside a virtual machine:

::

    Flushing output buffer. 10811.29 messages/s
    Flushing output buffer. 11375.65 messages/s
    Flushing output buffer. 11930.45 messages/s
    Flushing output buffer. 11970.28 messages/s
    Flushing output buffer. 11016.74 messages/s
    Flushing output buffer. 11852.67 messages/s
    Flushing output buffer. 11833.07 messages/s
    Flushing output buffer. 11599.32 messages/s
    Flushing output buffer. 11800.12 messages/s
    Flushing output buffer. 12026.89 messages/s
    Flushing output buffer. 12287.26 messages/s
    Flushing output buffer. 11538.44 messages/s

For higher performance you can run kafka-influxdb on PyPy3. Currently this gives me around 50k msgs/s in my benchmarks.



Supported formats
-----------------

| You can write a custom encoder to support any input and output format (even fancy things like Protobuf). Look at the examples inside the ``encoder`` directory to get started. The following formats are officially supported:

Input formats
~~~~~~~~~~~~~

-  `Collectd Graphite ASCII format <https://collectd.org/wiki/index.php/Graphite>`_:
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

   mydatacenter.myhost.load.load.shortterm 0.45 1436357630

-  `Collectd JSON format <https://collectd.org/wiki/index.php/JSON>`_:
.. code-block:: json

  [{
      "values":[
         0.6
      ],
      "dstypes":[
         "gauge"
      ],
      "dsnames":[
         "value"
      ],
      "time":1444745144.824,
      "interval":10.000,
      "host":"xx.example.internal",
      "plugin":"cpu",
      "plugin_instance":"1",
      "type":"percent",
      "type_instance":"system"
   }]


Output formats
~~~~~~~~~~~~~~

-  `InfluxDB 0.9.x line protocol format <https://influxdb.com/docs/v0.9/write_protocols/line.html>`_:
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

   load_load_shortterm,datacenter=mydatacenter,host=myhost value="0.45" 1436357630

-  `InfluxDB 0.8.x JSON format <https://influxdb.com/docs/v0.8/api/reading_and_writing_data.html#writing-data-through-http>`_ (deprecated)


Configuration
-------------

| Take a look at the ``config-example.yaml`` to find out how to create a config file.
| You can overwrite the settings from the commandline. The following parameters are allowed:

========================================================= =================================================================================================
Option                                                    Description
========================================================= =================================================================================================
``kafka:``                                                       
``  host: "127.0.0.1:9092"``                                示例：'mykafkaClusterNode1.com:9092,mykafkaClusterNode2.com:9092'
``  topic: "metrics"``
``  group: "kafka-influxdb"``
``  zookeeper: "127.0.0.1:2181"``                           示例：    'myZkClusterNode1.com:2181,myZkClusterNode2.com:2181'
``influxdb:``
``  host: "influxdb"``                                      示例：     'myinfluxdbNode1.com:8086,myinfluxdbNode2.com:8086'
``  port: 8086``
``  user: "root"``
``  password: "root"``
``  dbname: "metrics"``
``  hosts``                                                 influxdb://usr:pwd@host1:8086,usr:pwd@host2:8086/db_name
``  use_ssl: false``
``  verify_ssl: False``
``  timeout: 5``
``  use_udp: False``
``  retention_policy: "default"``
``  time_precision: "s"``
``encoder: "kafka_influxdb.encoder.echo_encoder"``          kafka_influxdb.encoder.collectd_graphite_encoder
`` ``                                                       kafka_influxdb.encoder.collectd_graphite_encoder_original
`` ``                                                       kafka_influxdb.encoder.echo_encoder  不做数据处理
`` ``                                                       kafka_influxdb.encoder.echo_telegraf_encoder  接受telegraf数据
``benchmark: false``
``buffer_size: 1000``
``statistics: false``
``verbose: 0``                                              1 、info  2、debug
``logfile: "/var/log/raysdata/kafka_influxdb.log"``          "/var/log/raysdata/kafka_influxdb.log"
========================================================= =================================================================================================


.. |Build Status| image:: https://travis-ci.org/mre/kafka-influxdb.svg?branch=master
   :target: https://travis-ci.org/mre/kafka-influxdb
.. |Coverage Status| image:: https://coveralls.io/repos/mre/kafka-influxdb/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/mre/kafka-influxdb?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/mre/kafka-influxdb/badges/gpa.svg
   :target: https://codeclimate.com/github/mre/kafka-influxdb
   :alt: Code Climate
.. |PyPi Version| image:: https://badge.fury.io/py/kafka_influxdb.svg
   :target: https://badge.fury.io/py/kafka_influxdb
.. |Downloads| image:: https://img.shields.io/pypi/dd/kafka-influxdb.svg
   :target: https://pypi.python.org/pypi/kafka-influxdb/
   :alt: pypi downloads per day
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/kafka-influxdb.svg
   :target: https://pypi.python.org/pypi/coveralls/
   :alt: Supported Python Versions
   
