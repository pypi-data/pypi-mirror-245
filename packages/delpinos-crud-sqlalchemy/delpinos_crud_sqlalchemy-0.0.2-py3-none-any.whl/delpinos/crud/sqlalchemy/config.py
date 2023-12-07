# -*- coding: utf-8 -*-
# pylint: disable=C0114

import os
from typing import Any, Dict
from urllib.parse import quote_plus

from delpinos.crud.sqlalchemy.configuration.functions import (
    build_sqlalchemy_connection_uri,
)

DEFAULT_DATABASE_DRIVER = "postgresql+psycopg2"
DEFAULT_DATABASE_USER = "postgres"
DEFAULT_DATABASE_PASSWORD = "postgres"
DEFAULT_DATABASE_HOST = "localhost"
DEFAULT_DATABASE_PORT = "5432"
DEFAULT_DATABASE_NAME = "postgres"
DEFAULT_DATABASE_ARGS = ""


config: Dict[str, Any] = {
    "sqlalchemy": {
        "connection": {
            "uri": build_sqlalchemy_connection_uri(),
        },
    },
}
