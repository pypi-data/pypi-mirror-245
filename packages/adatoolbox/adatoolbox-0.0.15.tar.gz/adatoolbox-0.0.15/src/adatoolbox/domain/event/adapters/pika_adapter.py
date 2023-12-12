import time
import json
from loguru import logger

import pika
from pika.exceptions import AMQPConnectionError


class PikaBaseAdapter:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        port: int,
        protocol: str = 'amqp',
        virtual_host: str = '/',
        reconnect_tries: int = 20,
        reconnect_delay: int = 5,
    ):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.protocol = protocol
        self.virtual_host = virtual_host
        self.reconnect_tries = reconnect_tries
        self.reconnect_delay = reconnect_delay

        self._init_connection_parameters()
        self._connect()


    def _connect(self):
        tries = 0
        while True:
            try:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                if self.connection.is_open:
                    break
            except AMQPConnectionError as amqp_exception:
                delay = tries * tries
                delay = min(delay, 60)
                time.sleep(delay)
                tries += 1
                if tries == self.reconnect_tries:
                    raise AMQPConnectionError(amqp_exception) from amqp_exception
                
    
    def _init_connection_parameters(self):
        self.credentials = pika.PlainCredentials(self.username, self.password)
        self.parameters = pika.ConnectionParameters(
            self.host,
            int(self.port),
            self.virtual_host,
            self.credentials,
        )
