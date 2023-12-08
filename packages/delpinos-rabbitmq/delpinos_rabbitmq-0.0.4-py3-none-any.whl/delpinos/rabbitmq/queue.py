# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205,W0613,R0801

import logging
from typing import Any, Dict, List
from pika.frame import Method
from pika.channel import Channel
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqQueue(RabbitmqChannel):
    def setup(self, **kwargs):
        super().setup()
        self.config.setup_queue()


class RabbitmqQueueDeclare(RabbitmqQueue):
    _queue_is_declared: bool

    def __init__(self, **kwargs):
        self._queue_is_declared = False
        super().__init__(**kwargs)

    @property
    def is_declared_queue(self) -> bool:
        return bool(self._queue_is_declared)

    def waiting_declared_queue(self):
        while not self.is_declared_queue:
            continue
        return self

    def on_open_channel_ok(self):
        self.queue_declare()

    def queue_declare(self):
        LOGGER.info("Declaring queue: %s", self.config.queue)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.queue_declare(
                queue=self.config.queue,
                passive=self.config.queue_passive,
                durable=self.config.queue_durable,
                exclusive=self.config.queue_exclusive,
                auto_delete=self.config.queue_auto_delete,
                arguments=self.config.queue_arguments,
                callback=self.on_queue_declare_ok,
            )

    def on_queue_declare_ok(self, method_frame: Method):
        LOGGER.info("Queue declared: %s", self.config.queue)
        self.set("declared_queue", True)

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_declared_queue()


class RabbitmqQueueBind(RabbitmqQueue):
    _binded_queue: bool

    def __init__(self, **kwargs):
        self._binded_queue = False
        super().__init__(**kwargs)

    def setup(self, **kwargs):
        super().setup()
        self.config.setup_queue_bind(**kwargs)

    @property
    def is_binded_queue(self) -> int:
        return bool(self._binded_queue)

    def waiting_binded_queue(self):
        while not self.is_binded_queue:
            continue
        return self

    def on_open_channel_ok(self):
        self.queue_bind()

    def queue_bind(self):
        LOGGER.info("Binding queue: %s", self.config.queue)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.queue_bind(
                queue=self.config.queue,
                exchange=self.config.queue_bind_exchange,
                routing_key=self.config.queue_bind_routing_key,
                arguments=self.config.queue_bind_arguments,
                callback=self.on_queue_bind_ok,
            )

    def on_queue_bind_ok(self, method_frame: Method):
        LOGGER.info("Queue binded: %s", self.config.queue)
        self.set("binded_queue", True)

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_binded_queue()
