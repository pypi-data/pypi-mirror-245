# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,R0801

import logging
from pika.channel import Channel
from pika.frame import Method
from delpinos.rabbitmq.channel import RabbitmqChannel


LOGGER = logging.getLogger(__name__)


class RabbitmqExchangeDeclare(RabbitmqChannel):
    _exchange_is_declared: bool

    def __init__(self, **kwargs):
        self._exchange_is_declared = False
        super().__init__(**kwargs)

    def setup(self, **kwargs):
        super().setup()
        self.config.setup_exchange(**kwargs)

    def waiting_exchange_is_declared(self):
        while not self._exchange_is_declared:
            continue
        return self

    def on_open_channel_ok(self):
        self.exchange_declare()

    def exchange_declare(self):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declare_ok method will
        be invoked by pika.
        """

        LOGGER.info("Declaring exchange: %s", self.config.exchange)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.exchange_declare(
                exchange=self.config.exchange,
                exchange_type=self.config.exchange_type,
                passive=self.config.exchange_passive,
                durable=self.config.exchange_durable,
                auto_delete=self.config.exchange_auto_delete,
                internal=self.config.exchange_internal,
                arguments=self.config.exchange_arguments,
                callback=self.on_exchange_declare_ok,
            )

    def on_exchange_declare_ok(self, method_frame: Method):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame
        :param dict: Config

        """
        LOGGER.info("Exchange declared: %s", self.config.exchange)
        self.__exchange_is_declared = True

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_exchange_is_declared()


class RabbitmqExchangeBind(RabbitmqChannel):
    _exchange_is_binded: bool

    def __init__(self, **kwargs):
        self._exchange_is_binded = False
        super().__init__(**kwargs)

    def setup(self, **kwargs):
        super().setup()
        self.config.setup_exchange_bind(**kwargs)

    def waiting_exchange_is_binded(self):
        while not self._exchange_is_binded:
            continue
        return self

    def on_open_channel_ok(self):
        self.exchange_bind()

    def exchange_bind(self):
        """Setup the exchange bind on RabbitMQ. When it is complete, the on_exchange_bind_ok method will
        be invoked by pika.
        """

        LOGGER.info("Binding exchange: %s", self.config.exchange)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.exchange_bind(
                destination=self.config.exchange_bind_destination,
                source=self.config.exchange_bind_source,
                routing_key=self.config.exchange_bind_routing_key,
                arguments=self.config.exchange_bind_arguments,
                callback=self.on_exchange_bind_ok,
            )

    def on_exchange_bind_ok(self, method_frame: Method):
        """Invoked by pika when the Exchange.Bind method has completed. At this
        point we will set the prefetch count for the channel.

        :param pika.frame.Method method_frame: Method: The Exchange.BindOk response frame
        :param dict: Config

        """

        LOGGER.info("Exchange binded: %s", self.config.exchange)
        self._exchange_is_binded = True

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_exchange_is_binded()
