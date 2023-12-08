# -*- coding: utf-8 -*-
# pylint: disable=C0114

import json
from typing import Dict
from sqlalchemy import FromClause

from sqlalchemy.schema import Column

from delpinos.crud.core.domain.entities import BaseEntity


class AliasColumn(Column):
    __alias: str

    def __init__(self, *args, **kwargs):
        __alias = kwargs.pop("alias", None)
        super().__init__(*args, **kwargs)
        self.__alias = __alias or self.name

    @property
    def alias(self):
        return self.__alias


class SqlAlchemyModel:
    __table__: FromClause

    def __init__(self, **kwargs):
        self.__dict__["__changes__"] = {}
        self.__dict__["__changed__"] = {}
        self.__dict__["__values__"] = {}
        self.__dict__["__sets__"] = {}
        for attr in self.get_attributes().keys():
            self.__dict__["__sets__"][attr] = False
            self.__dict__["__changed__"][attr] = False
            if hasattr(kwargs, attr):
                value = kwargs.get(attr)
                self.__dict__["__sets__"][attr] = True
                self.__dict__["__values__"][attr] = value
        super().__init__(**kwargs)

    def get_attributes(self) -> Dict[str, str]:
        attributes = {}
        for column in self.__table__.columns:
            name = str(column.name)
            if not hasattr(self, name):
                continue
            if isinstance(column, AliasColumn):
                attributes[name] = column.alias
            elif isinstance(column, Column):
                attributes[name] = column.name
        return attributes

    def get_changes(self) -> Dict[str, tuple]:
        changes = {}
        attributes = self.get_attributes().keys()
        for field in attributes:
            if self.has_changed(field):
                init = self.__dict__["__values__"].get(field)
                value = self.__dict__.get(field, init)
                changes[field] = (init, value)
        return changes

    def has_changed(self, *args) -> bool:
        if "__values__" not in self.__dict__:
            self.__dict__["__values__"] = {}
        if len(args) == 0:
            args = self.get_attributes().keys()
        for field in args:
            init = self.__dict__["__values__"].get(field)
            value = self.__dict__.get(field, init)
            if value != init:
                return True
        return False

    def model_dump(self, by_alias: bool = True, exclude_unset: bool = False):
        values = {}
        attributes = self.get_attributes()
        for name, alias in attributes.items():
            if exclude_unset and not self.__dict__["__sets__"].get(name):
                continue
            value = getattr(self, name)
            if by_alias:
                values[alias] = value
            else:
                values[name] = value
        return values

    def model_dump_json(self, by_alias: bool = True, exclude_unset: bool = False):
        return json.dumps(self.model_dump(by_alias, exclude_unset), default=str)

    def merge(self, *args, **kwargs):
        obj_dict = {}
        by_alias = bool(kwargs.get("by_alias"))
        attributes = self.get_attributes()
        for obj in args:
            try:
                if isinstance(obj, (SqlAlchemyModel, BaseEntity)):
                    obj_dict.update(
                        obj.model_dump(by_alias=by_alias, exclude_unset=True)
                    )
                elif isinstance(obj, dict):
                    obj_dict.update(obj)
            except Exception:
                continue
        for column in attributes.keys():
            setattr(self, column, obj_dict.get(column, getattr(self, column)))
