# -*- coding: utf-8 -*-

import logging
import influxdb

from influxdb import InfluxDBClusterClient

class InfluxDBWriter(object):
    DEFAULT_HEADERS = {
        'Content-type': 'application/octet-stream',
        'Accept': 'text/plain'
    }

    def __init__(self,
                 hosts,
                 host,
                 port,
                 user,
                 password,
                 dbname,
                 use_ssl=False,
                 verify_ssl=False,
                 timeout=5,
                 use_udp=False,
                 retention_policy=None,
                 time_precision=None):
        """
        Initialize InfluxDB writer
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.use_ssl = use_ssl
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.use_udp = use_udp
        self.retention_policy = retention_policy
        self.time_precision = time_precision
        self.hosts=hosts
        # self.params = {'db': self.dbname}
        self.params = {'db': self.dbname}
        self.headers = self.DEFAULT_HEADERS
        if time_precision:
            self.params['precision'] = time_precision
        if retention_policy:
            self.params['rp'] = retention_policy

        self.client = self.create_cluster()
        logging.info("Creating database %s if not exists", dbname)

    def create_client(self):
        """
        Create an InfluxDB client
        """
        return influxdb.InfluxDBClient(self.host,
                                       self.port,
                                       self.user,
                                       self.password,
                                       self.dbname,
                                       self.use_ssl,
                                       self.verify_ssl,
                                       self.timeout,
                                       self.use_udp,
                                       self.port)

    def create_database(self, dbname):
        """
        Initialize the given database
        :param dbname:
        """
        self.client.create_database(dbname)
        
    @staticmethod
    def getHosts(host):
        ps=host.split(",")
        rs=[]
        for p in ps:
            h,port=p.split(":")
            rs.append((h,int(port)))
        return rs
        
    def create_cluster(self):
        logging.info("connecting to influxdb at :%s",self.hosts)
        self.client = InfluxDBClusterClient.from_DSN(self.hosts,
                               ssl= self.use_ssl,
                               verify_ssl=self.verify_ssl,
                               timeout=self.timeout,
                               use_udp=self.use_udp)
        return self.client
    def write(self, msg, params=None, expected_response_code=204):
        """
        Write messages to InfluxDB database.
        Expects messages in line protocol format.
        See https://influxdb.com/docs/v0.9/write_protocols/line.html
        :param expected_response_code:
        :param params:
        :param msg:
        """
        #print "msg:"+"\n".join(msg)
        if not params:
            # Use defaults
            params = self.params
            
        try:
            self.client.request(url='write',
                                method='POST',
                                params=params,
                                data="\n".join(msg),
                                expected_response_code=expected_response_code,
                                headers=self.headers
                                )
            logging.debug("write data msg: %s", msg)
        except Exception as e:
            logging.warning("Cannot write data points: %s", e)
            logging.warning("Cannot write data msg: %s", "\n".join(msg))
            return False
        return True

    def write08(self):
        """
        TODO: Write in InfluxDB legacy 08 format:
        data = [
            {
                "name": "cpu_load_short",
                "columns": [
                    "value"
                ]
                "points": [
                    [
                        12
                    ]
                ],
            }
        ]
        client.write_points(data, time_precision='s', *args, **kwargs):
        """
        raise NotImplementedError
