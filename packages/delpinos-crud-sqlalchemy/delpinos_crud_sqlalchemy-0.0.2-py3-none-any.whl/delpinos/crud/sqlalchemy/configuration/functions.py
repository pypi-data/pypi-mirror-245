# -*- coding: utf-8 -*-
# pylint: disable=C0114

import os
from typing import Any, Dict
from urllib.parse import quote_plus
from delpinos.core.functions.dict_function import dicts_merge


SQLALCHEMY_CONNECTION_DEFAULT_DRIVER = "postgresql+psycopg2"
SQLALCHEMY_CONNECTION_DEFAULT_USER = "postgres"
SQLALCHEMY_CONNECTION_DEFAULT_PASSWORD = "postgres"
SQLALCHEMY_CONNECTION_DEFAULT_HOST = "localhost"
SQLALCHEMY_CONNECTION_DEFAULT_PORT = "5432"
SQLALCHEMY_CONNECTION_DEFAULT_DATABASE = "postgres"
SQLALCHEMY_CONNECTION_DEFAULT_ARGS = ""
SQLALCHEMY_CONNECTION_DEFAULT_PREFIX = "SQLALCHEMY_CONNECTION_"


def build_sqlalchemy_connection_uri(
    prefix: str | None = None,
    default: Dict[str, Any] | None = None,
    **kwargs,
) -> str:
    prefix = prefix or SQLALCHEMY_CONNECTION_DEFAULT_PREFIX
    default = dicts_merge(default if isinstance(default, dict) else {}, kwargs)
    uri = os.getenv(f"{prefix}URI", default.get("uri"))
    if uri and "://" in uri:
        return uri
    driver = os.getenv(f"{prefix}DRIVER", SQLALCHEMY_CONNECTION_DEFAULT_DRIVER)
    user = str(
        os.getenv(
            f"{prefix}USER", default.get("user", SQLALCHEMY_CONNECTION_DEFAULT_USER)
        )
    )
    password = str(
        os.getenv(
            f"{prefix}PASSWORD",
            default.get("password", SQLALCHEMY_CONNECTION_DEFAULT_PASSWORD),
        )
    )
    host = str(
        os.getenv(f"{prefix}HOST", default.get("host"))
        or SQLALCHEMY_CONNECTION_DEFAULT_HOST
    )
    port = str(
        os.getenv(f"{prefix}PORT", default.get("port"))
        or SQLALCHEMY_CONNECTION_DEFAULT_PORT
    )
    database = str(
        os.getenv(
            f"{prefix}DATABASE",
            default.get("database", SQLALCHEMY_CONNECTION_DEFAULT_DATABASE),
        )
    )
    args = str(
        os.getenv(
            f"{prefix}ARGS", default.get("args", SQLALCHEMY_CONNECTION_DEFAULT_ARGS)
        )
    )
    uri_parts = [
        driver,
        "://",
        user,
        ":",
        quote_plus(password),
        "@",
        host,
        ":",
        port,
        "/",
        quote_plus(database),
        "?",
        args,
    ]
    return ("".join(uri_parts)).replace("??", "?").strip("?").strip("/")


def build_sqlalchemy_connection_config(
    prefix: str | None = None,
    default: Dict[str, Any] | None = None,
    **kwargs,
) -> Dict[str, Any]:
    prefix = prefix or SQLALCHEMY_CONNECTION_DEFAULT_PREFIX
    default = dicts_merge(default if isinstance(default, dict) else {}, kwargs)
    default_connection_parameters = default.get("connection_parameters")
    default_connection_parameters = (
        default_connection_parameters
        if isinstance(default_connection_parameters, dict)
        else {}
    )
    return {
        "connection": {"uri": build_sqlalchemy_connection_uri(prefix)},
    }
