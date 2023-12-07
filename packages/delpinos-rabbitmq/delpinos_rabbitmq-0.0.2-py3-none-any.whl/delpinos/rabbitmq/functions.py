# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613

import os
from typing import Any, Dict
from urllib.parse import quote_plus
from delpinos.core.functions.dict_function import dicts_merge


RABBITMQ_CONNECTION_DEFAULT_PREFIX = "RABBITMQ_CONNECTION_"
RABBITMQ_CONNECTION_DEFAULT_USER = "guest"
RABBITMQ_CONNECTION_DEFAULT_PASSWORD = "guest"
RABBITMQ_CONNECTION_DEFAULT_HOST = "localhost"
RABBITMQ_CONNECTION_DEFAULT_PORT = "5672"
RABBITMQ_CONNECTION_DEFAULT_VHOST = "/"
RABBITMQ_CONNECTION_DEFAULT_ARGS = ""
RABBITMQ_CONNECTION_DEFAULT_PREFIX = "RABBITMQ_CONNECTION_"


def build_rabbitmq_connection_uri(
    prefix: str | None = None,
    default: Dict[str, Any] | None = None,
    **kwargs,
) -> str:
    prefix = prefix or RABBITMQ_CONNECTION_DEFAULT_PREFIX
    default = dicts_merge(default if isinstance(default, dict) else {}, kwargs)
    uri = os.getenv(f"{prefix}URI", default.get("uri"))
    if uri and "://" in uri:
        return uri
    user = str(
        os.getenv(
            f"{prefix}USER", default.get("user", RABBITMQ_CONNECTION_DEFAULT_USER)
        )
    )
    password = str(
        os.getenv(
            f"{prefix}PASSWORD",
            default.get("password", RABBITMQ_CONNECTION_DEFAULT_PASSWORD),
        )
    )
    host = str(
        os.getenv(f"{prefix}HOST", default.get("host"))
        or RABBITMQ_CONNECTION_DEFAULT_HOST
    )
    port = str(
        os.getenv(f"{prefix}PORT", default.get("port"))
        or RABBITMQ_CONNECTION_DEFAULT_PORT
    )
    vhost = str(
        os.getenv(
            f"{prefix}VHOST", default.get("vhost", RABBITMQ_CONNECTION_DEFAULT_VHOST)
        )
    )
    args = str(
        os.getenv(
            f"{prefix}ARGS", default.get("args", RABBITMQ_CONNECTION_DEFAULT_ARGS)
        )
    )
    uri_parts = [
        "amqp://",
        user,
        ":",
        quote_plus(password),
        "@",
        host,
        ":",
        port,
        "/",
        quote_plus(vhost),
        "?",
        args,
    ]
    return ("".join(uri_parts)).replace("??", "?").strip("?").strip("/")


def build_rabbitmq_connection_config(
    prefix: str | None = None,
    default: Dict[str, Any] | None = None,
    **kwargs,
) -> Dict[str, Any]:
    prefix = prefix or RABBITMQ_CONNECTION_DEFAULT_PREFIX
    default = dicts_merge(default if isinstance(default, dict) else {}, kwargs)
    default_connection_parameters = default.get("connection_parameters")
    default_connection_parameters = (
        default_connection_parameters
        if isinstance(default_connection_parameters, dict)
        else {}
    )
    return {
        "connection_parameters": {
            "uri": build_rabbitmq_connection_uri(prefix, default_connection_parameters)
        },
    }
