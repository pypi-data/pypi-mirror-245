#!/usr/bin/env python

from delpinos.rabbitmq.queue import RabbitmqQueueBind
from delpinos.rabbitmq.queue import RabbitmqQueueDeclare
from delpinos.rabbitmq.exchange import RabbitmqExchangeBind
from delpinos.rabbitmq.exchange import RabbitmqExchangeDeclare


def setup_exchange_declare(config: dict):
    obj = RabbitmqExchangeDeclare(**config)
    obj.run(True)
    obj.stop()


def setup_exchange_bind(config: dict):
    obj = RabbitmqExchangeBind(**config)
    obj.run(True)
    obj.stop()


def setup_queue_declare(config: dict):
    obj = RabbitmqQueueDeclare(**config)
    obj.run(True)
    obj.stop()


def setup_queue_bind(config: dict):
    obj = RabbitmqQueueBind(**config)
    obj.run(True)
    obj.stop()
