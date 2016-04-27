DEFAULT_CONFIG = {
    'kafka': {
        'host': '127.0.0.1:9092',
        'topic': 'my_topic',
        'group': 'kafka-influxdb',
        'zookeeper':'127.0.0.1:2181'
    },
    'influxdb': {
        'host': '127.0.0.1：8086',
        'port': 8086,
        'user': 'root',
        'password': 'root',
        'dbname': 'metrics',
        'use_ssl': False,
        'verify_ssl': False,
        'timeout': 5,
        'use_udp': False,
        'retention_policy': 'default',
        'time_precision': 's'
    },
    'encoder': 'kafka_influxdb.encoder.collectd_graphite_encoder_original',
    'buffer_size': 1000,
    'configfile': None,
    'c': None,
    'statistics': False,
    's': False,
    'benchmark': False,
    'b': False,
    'verbose': 0,
    'v': 0,
    'logfile':'/var/log/raysdata/kafka_influxdb.log'
}
