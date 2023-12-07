# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613

import logging
from pika import SelectConnection
from pika.frame import Method
from pika.channel import Channel
from pika.spec import BasicProperties, Basic
from delpinos.rabbitmq.connection import RabbitmqConnection, RabbitmqConnectionWrapper


LOGGER = logging.getLogger(__name__)


class RabbitmqChannel(RabbitmqConnection):
    @property
    def channel(self) -> Channel | None:
        return self.variables.get("channel")

    @property
    def channel_number(self) -> int | None:
        return self.variables.get("channel_number")

    @property
    def is_open_channel(self) -> bool:
        return isinstance(self.channel, Channel) and self.channel.is_open

    @property
    def is_closed_channel(self) -> bool:
        return not isinstance(self.channel, Channel) or self.channel.is_closed

    @property
    def is_closing_channel(self) -> bool:
        return not isinstance(self.channel, Channel) or self.channel.is_closing

    def waiting_channel(self):
        self.waiting_connection()
        while not isinstance(self.channel, Channel):
            continue
        return self

    def waiting_open_channel(self):
        self.waiting_channel()
        while not (isinstance(self.channel, Channel) and self.channel.is_open):
            continue
        return self

    def waiting_closed_channel(self):
        if isinstance(self.channel, Channel):
            while not self.channel.is_closed:
                continue
        return self

    def on_open_connection_ok(self):
        self.open_channel()

    def open_channel(self):
        try:
            self.waiting_open_connection()
            connection = self.connection
            if isinstance(connection, RabbitmqConnectionWrapper):
                connection.waiting_connection()
                select_connection = connection.connection
                LOGGER.warn("Creating a new channel")
                if isinstance(select_connection, SelectConnection):
                    select_connection.channel(
                        channel_number=self.channel_number,
                        on_open_callback=self.on_open_channel,
                    )
        except Exception as err:
            self.on_open_channel_error(err)

    def on_open_channel(self, channel: Channel):
        LOGGER.warn("Channel opened")
        self.variables.set("channel", channel)
        self.variables.set("channel_number", channel.channel_number)
        self.on_open_channel_ok()

    def on_open_channel_ok(self):
        pass

    def on_open_channel_error(self, err: Exception):
        raise err

    def close_channel(self):
        if isinstance(self.channel, Channel):
            LOGGER.warn("Closing the channel")
            self.channel.close()
            self.waiting_closed_channel()
            self.variables.set("channel", None)
            self.variables.set("channel_number", None)
            LOGGER.warn("Channel closed")

    def basic_ack(self, delivery_tag=None, multiple=None):
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_ack(
                delivery_tag=int(delivery_tag or 0), multiple=multiple is True
            )

    def basic_nack(self, delivery_tag=None, multiple=None, requeue=None):
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_nack(
                delivery_tag=int(delivery_tag or 0),
                multiple=multiple is True,
                requeue=requeue or True,
            )

    def basic_reject(self, delivery_tag=None, requeue=None):
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_reject(
                delivery_tag=int(delivery_tag or 0), requeue=requeue or True
            )

    def basic_cancel(self, consumer_tag=None, callback=None):
        callback = self.default_on_event_ok if not callable(callback) else callback
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_cancel(
                consumer_tag=consumer_tag or "", callback=callback
            )

    def basic_get(self, queue, callback=None, auto_ack=None):
        callback = self.default_get_callback if not callable(callback) else callback
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_get(
                queue=queue, callback=callback, auto_ack=auto_ack is True
            )

    def basic_recover(self, requeue=False, callback=None):
        callback = self.default_on_event_ok if not callable(callback) else callback
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_recover(requeue=requeue, callback=callback)

    def basic_qos(
        self, prefetch_size=0, prefetch_count=0, global_qos=False, callback=None
    ):
        callback = self.default_on_event_ok if not callable(callback) else callback
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_qos(
                prefetch_size=int(prefetch_size or 0),
                prefetch_count=int(prefetch_count or 1),
                global_qos=global_qos is True,
                callback=callback,
            )

    def basic_consume(
        self,
        queue,
        on_message_callback,
        auto_ack=None,
        exclusive=None,
        consumer_tag=None,
        arguments=None,
        callback=None,
    ):
        callback = self.default_on_event_ok if not callable(callback) else callback
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_consume(
                queue=queue,
                on_message_callback=on_message_callback,
                auto_ack=auto_ack is True,
                exclusive=exclusive is True,
                consumer_tag=consumer_tag,
                arguments=arguments,
                callback=callback,
            )

    def basic_publish(
        self,
        exchange: str,
        routing_key: str,
        body: bytes,
        properties: BasicProperties | None = None,
        mandatory: bool = False,
    ):
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body,
                properties=properties or BasicProperties(),
                mandatory=mandatory is True,
            )

    def default_get_callback(
        self,
        channel: Channel,
        method: Basic.GetOk,
        properties: BasicProperties,
        body: bytes,
    ):
        LOGGER.warn("Get message: %s", body)

    def default_on_event_ok(self, method_frame: Method):
        pass

    def health_check(self) -> tuple:
        try:
            health_check = super().health_check()
            if not isinstance(health_check, tuple):
                raise Exception("Unhealth")
            if not health_check[0]:
                return health_check
            if self.is_closed_channel:
                raise Exception("Rabbitmq channel is closed")
            if not self.is_open_channel:
                raise Exception("Rabbitmq channel is not open")
            return True, "Success"
        except Exception as err:
            return False, str(err)

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_open_channel()

    def stop(self, blocking: bool = False):
        super().stop(blocking)
        if blocking:
            self.waiting_closed_channel()
