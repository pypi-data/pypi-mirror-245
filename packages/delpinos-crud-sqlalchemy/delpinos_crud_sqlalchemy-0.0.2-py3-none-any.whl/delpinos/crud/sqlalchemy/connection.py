# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import List
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker as SessionMaker,
    scoped_session as ScopedSession,
)
from delpinos.core.config_object import ConfigObject
from delpinos.core.factories.factory import Factory


class SqlAlchemyConnectionConfig(ConfigObject):
    @property
    def connection_uri(self) -> str:
        return self.get("uri", tp=str)


class SqlAlchemyConnection(Factory):
    config: SqlAlchemyConnectionConfig

    @property
    def config_class(self):
        return SqlAlchemyConnectionConfig

    @property
    def config_key(self) -> str:
        return "sqlalchemy.connection"

    def add_factories(self):
        self.add_factory(
            "sqlalchemy.connection.engine",
            lambda _: self.build_engine(),
        )
        self.add_factory(
            "sqlalchemy.connection.scoped_session",
            lambda _: self.build_scoped_session(),
        )
        self.add_factory(
            "sqlalchemy.connection.sessionmaker",
            lambda _: self.build_sessionmaker(),
        )

    @property
    def engine(self) -> Engine:
        return self.instance(
            "sqlalchemy.connection.engine",
            Engine,
        )

    @property
    def scoped_session(self) -> ScopedSession:
        return self.instance(
            "sqlalchemy.connection.scoped_session",
            ScopedSession,
        )

    @property
    def sessionmaker(self) -> SessionMaker:
        return self.instance(
            "sqlalchemy.connection.sessionmaker",
            SessionMaker,
        )

    def new_session(self) -> Session:
        return self.scoped_session()

    def build_engine(self) -> Engine:
        return create_engine(self.config.connection_uri)

    def build_sessionmaker(
        self,
        autocommit: bool = False,
        autoflush: bool = False,
        engine: Engine | None = None,
    ) -> SessionMaker:
        engine = engine if isinstance(engine, Engine) else self.engine
        return SessionMaker(
            autocommit=autocommit,
            autoflush=autoflush,
            bind=engine,
        )

    def build_scoped_session(
        self,
        sessionmaker: SessionMaker | None = None,
    ) -> ScopedSession:
        sessionmaker = (
            sessionmaker
            if isinstance(sessionmaker, SessionMaker)
            else self.sessionmaker
        )
        return ScopedSession(sessionmaker)
