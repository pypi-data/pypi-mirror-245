# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,R0801

import logging
import json
from typing import Any, Dict
from pika.spec import BasicProperties
from delpinos.rabbitmq.channel import RabbitmqChannel


LOGGER = logging.getLogger(__name__)


class RabbitmqProducer(RabbitmqChannel):
    def setup(self, **kwargs):
        super().setup()
        self.config.setup_producer(**kwargs)

    def publish(
        self,
        body: str | Dict[str, Any] | bytes,
        exchange: str | None = None,
        routing_key: str | None = None,
        properties: BasicProperties | Dict[str, Any] | None = None,
        mandatory: bool | None = None,
    ):
        exchange = exchange if exchange else self.config.producer_exchange
        routing_key = routing_key if routing_key else self.config.producer_routing_key
        properties = (
            BasicProperties(**properties)
            if isinstance(properties, dict)
            else properties
            if isinstance(properties, BasicProperties)
            else self.config.producer_properties
        )
        properties = (
            BasicProperties(**properties)
            if isinstance(properties, dict)
            else properties
        )
        mandatory = bool(
            mandatory if mandatory is not None else self.config.producer_mandatory
        )
        if isinstance(body, bytes):
            new_body = body
        elif isinstance(body, dict):
            new_body = json.dumps(body, default=str).encode("utf-8")
        else:
            new_body = str(body).encode("utf-8")
        return self.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=new_body,
            properties=properties,
            mandatory=mandatory,
        )
