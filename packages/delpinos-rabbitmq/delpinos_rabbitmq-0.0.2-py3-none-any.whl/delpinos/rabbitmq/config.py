# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613

import os
import json
from typing import Any, Dict, List, Type
from pika.spec import BasicProperties
from pika.connection import Parameters, URLParameters
from pika.exchange_type import ExchangeType
from delpinos.core.config_object import ConfigObject

DEFAULT_RABBITMQ_CONNECTION_RETRIES = 1000
DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT = 15


class RabbitmqConfig(ConfigObject):
    def setup_connection(self, **kwargs):
        parameters = self.get("connection_parameters")
        retries = self.get("connection_retries")
        timeout = self.get("connection_timeout")
        retries = int(
            retries
            if isinstance(retries, int)
            else DEFAULT_RABBITMQ_CONNECTION_RETRIES,
        )
        timeout = int(
            timeout
            if isinstance(timeout, int)
            else DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT,
        )
        if not isinstance(parameters, (Parameters, dict)):
            parameters = {}
        if isinstance(parameters, dict):
            uri = str(parameters.get("uri") or os.getenv("RABBITMQ_CONNECTION_URI"))
            parameters = URLParameters(uri)
        self.set("connection_retries", retries, tp=int)
        self.set("connection_retries", retries, tp=int)
        self.set("connection_timeout", timeout, tp=int)
        self.set("connection_rabbitmq_parameters", parameters, tp=Parameters)

    def setup_producer(self, **kwargs):
        pass

    def setup_consumer(self, **kwargs):
        consumer_queue = self.get("consumer_queue", tp=str)
        self.set("consumer_queue", consumer_queue)
        self.set("consumer_retries", int(self.get("consumer_retries") or 0))
        self.set("consumer_prefetch_size", int(self.get("consumer_prefetch_size") or 0))
        self.set(
            "consumer_prefetch_count", int(self.get("consumer_prefetch_count") or 1)
        )
        self.set("consumer_global_qos", bool(self.get("consumer_global_qos")))
        self.set("consumer_dlq_enable", bool(self.get("consumer_dlq_enable")))
        self.set(
            "consumer_dlq_exceptions",
            self.get("consumer_dlq_exceptions") or [json.JSONDecodeError],
        )
        self.set("consumer_dlq_enable", bool(self.get("consumer_dlq_enable")))
        self.set(
            "consumer_dlq_exchange", self.get("consumer_dlq_exchange") or "default"
        )
        self.set(
            "consumer_dlq_routing_key",
            self.get("consumer_dlq_routing_key") or consumer_queue + ".dlq",
        )
        self.set("consumer_header_retry", self.get("consumer_header_retry") or "retry")
        self.set(
            "consumer_header_exception",
            self.get("consumer_header_exception") or "exception",
        )

    def setup_exchange(self, **kwargs):
        self.set("exchange", self.get("exchange", tp=str))
        self.set("exchange_type", str(self.get("exchange_type") or ExchangeType.topic))
        self.set("exchange_passive", bool(self.get("exchange_passive")))
        self.set("exchange_durable", bool(self.get("exchange_durable")))
        self.set("exchange_auto_delete", bool(self.get("exchange_auto_delete")))
        self.set("exchange_internal", bool(self.get("exchange_internal")))
        self.set(
            "exchange_arguments", dict(self.get("exchange_arguments") or {}), tp=dict
        )

    def setup_exchange_bind(self, **kwargs):
        self.set(
            "exchange_bind_routing_key", self.get("exchange_bind_routing_key") or ""
        )
        self.set(
            "exchange_bind_destination", self.get("exchange_bind_destination", tp=str)
        )
        self.set("exchange_bind_source", self.get("exchange_bind_source", tp=str))
        self.set(
            "exchange_bind_arguments", dict(self.get("exchange_bind_arguments") or {})
        )

    def setup_queue(self, **kwargs):
        self.set("queue", self.get("queue", tp=str))
        self.set("queue_passive", bool(self.get("queue_passive")))
        self.set("queue_durable", bool(self.get("queue_durable")))
        self.set("queue_exclusive", bool(self.get("queue_exclusive")))
        self.set("queue_auto_delete", bool(self.get("queue_auto_delete")))
        self.set("queue_arguments", dict(self.get("queue_arguments") or {}), tp=dict)

    def setup_queue_bind(self, **kwargs):
        self.set("queue_bind_exchange", self.get("queue_bind_exchange", tp=str))
        self.set("queue_bind_arguments", dict(self.get("queue_bind_arguments") or {}))

    @property
    def connection_uri(self) -> int:
        return self.get("connection_uri", tp=str)

    @property
    def connection_timeout(self) -> int:
        return self.get("connection_timeout", tp=int)

    @property
    def connection_retries(self) -> int:
        return self.get("connection_retries", tp=int)

    @property
    def connection_attempt(self) -> int:
        return self.get("connection_attempt", tp=int)

    @property
    def connection_parameters(self) -> Parameters:
        return self.get("connection_rabbitmq_parameters", tp=Parameters)

    @property
    def consumer_queue(self) -> str:
        return self.get("consumer_queue", tp=str)

    @property
    def consumer_header_retry(self) -> str:
        return self.get("consumer_header_retry", tp=str)

    @property
    def consumer_header_exception(self) -> str:
        return self.get("consumer_header_exception", tp=str)

    @property
    def consumer_retries(self) -> int:
        return self.get("consumer_retries", tp=int)

    @property
    def consumer_prefetch_size(self) -> int:
        return self.get("consumer_prefetch_size", tp=int)

    @property
    def consumer_prefetch_count(self) -> int:
        return self.get("consumer_prefetch_count", tp=int)

    @property
    def consumer_global_qos(self) -> bool:
        return self.get("consumer_global_qos", tp=bool)

    @property
    def consumer_dlq_enable(self) -> bool:
        return self.get("consumer_dlq_enable", tp=bool)

    @property
    def consumer_dlq_exceptions(self) -> List[Type[Exception]]:
        return self.get("consumer_dlq_exceptions", tp=list)

    @property
    def consumer_dlq_exchange(self) -> str:
        return self.get("consumer_dlq_exchange")

    @property
    def consumer_dlq_routing_key(self) -> str:
        return self.get("consumer_dlq_routing_key")

    @property
    def exchange(self) -> str:
        return self.get("exchange", tp=str)

    @property
    def exchange_type(self) -> str:
        return self.get("exchange_type", tp=str)

    @property
    def exchange_passive(self) -> bool:
        return self.get("exchange_passive", tp=bool)

    @property
    def exchange_durable(self) -> bool:
        return self.get("exchange_durable", tp=bool)

    @property
    def exchange_auto_delete(self) -> bool:
        return self.get("exchange_auto_delete", tp=bool)

    @property
    def exchange_internal(self) -> bool:
        return self.get("exchange_internal", tp=bool)

    @property
    def exchange_arguments(self) -> Dict[str, Any]:
        return self.get("exchange_arguments", tp=dict)

    @property
    def exchange_bind_routing_key(self) -> str:
        return self.get("exchange_bind_routing_key", tp=str)

    @property
    def exchange_bind_destination(self) -> str:
        return self.get("exchange_bind_destination", tp=str)

    @property
    def exchange_bind_source(self) -> str:
        return self.get("exchange_bind_source", tp=str)

    @property
    def exchange_bind_arguments(self) -> Dict[str, Any]:
        return self.get("exchange_bind_arguments", tp=dict)

    @property
    def producer_exchange(self) -> str:
        return self.get("producer_exchange", tp=str)

    @property
    def producer_routing_key(self) -> str:
        return self.get("producer_routing_key", tp=str)

    @property
    def producer_mandatory(self) -> bool:
        return bool(self.get("producer_mandatory"))

    @property
    def producer_properties(self) -> BasicProperties | Dict[str, Any] | None:
        return self.get("producer_properties")

    @property
    def queue(self) -> str:
        return self.get("queue", tp=str)

    @property
    def queue_passive(self) -> bool:
        return bool(self.get("queue_passive"))

    @property
    def queue_durable(self) -> bool:
        return bool(self.get("queue_durable"))

    @property
    def queue_exclusive(self) -> bool:
        return bool(self.get("queue_exclusive"))

    @property
    def queue_auto_delete(self) -> bool:
        return bool(self.get("queue_auto_delete"))

    @property
    def queue_arguments(self) -> Dict[str, Any]:
        return self.get("queue_arguments", tp=dict)

    @property
    def queue_bind_exchange(self) -> str:
        return self.get("queue_bind_exchange", tp=str)

    @property
    def queue_bind_routing_key(self) -> str | None:
        return self.get("queue_bind_routing_key")

    @property
    def queue_bind_arguments(self) -> Dict[str, Any]:
        return self.get("queue_bind_arguments", tp=dict)
