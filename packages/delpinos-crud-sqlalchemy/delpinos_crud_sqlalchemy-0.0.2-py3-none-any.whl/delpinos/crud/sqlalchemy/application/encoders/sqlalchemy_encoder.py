# -*- coding: utf-8 -*-
# pylint: disable=C0114

import base64
from datetime import date, datetime
from typing import Any

from delpinos.core.factories.factory import Factory
from delpinos.crud.core.application.encoders.base_encoder import BaseEncoder
from delpinos.crud.sqlalchemy.application.models.sqlalchemy_model import SqlAlchemyModel


class SqlAlchemyEncoder(BaseEncoder):
    def add_factories(self):
        SqlAlchemyEncoder.add_factories_encoders(self)

    @classmethod
    def add_factories_encoders(cls, factory: Factory):
        factory.add_factory_impl("encoders.sqlalchemy", SqlAlchemyEncoder)

    def encode(self, obj: Any, **kwargs) -> str:
        if isinstance(obj, SqlAlchemyModel):
            return obj.model_dump_json(by_alias=True)
        if isinstance(obj, (dict, list, set)):
            obj = self.decode(obj)
        return super().encode(obj, **kwargs)

    def decode(self, obj: Any, **kwargs) -> Any:
        if isinstance(obj, bytes):
            return base64.b64encode(obj).decode("utf-8")
        if isinstance(obj, SqlAlchemyModel):
            return obj.model_dump(by_alias=True)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, dict):
            new_value = {}
            for key, value in obj.items():
                new_value[key] = self.decode(value)
            return new_value
        if isinstance(obj, (list, set)):
            return list(map(self.decode, obj))
        return super().decode(obj, **kwargs)
