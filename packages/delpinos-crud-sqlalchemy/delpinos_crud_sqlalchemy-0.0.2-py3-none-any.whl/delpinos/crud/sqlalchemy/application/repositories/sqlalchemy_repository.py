# -*- coding: utf-8 -*-
# pylint: disable=C0114

from typing import Any, Dict, List, Type

from delpinos.core.encoders import EncoderAbstract
from delpinos.core.exceptions.badrequest_exception import BadRequestException
from delpinos.core.exceptions.notfound_exception import NotFoundException
from delpinos.crud.core.domain.entities import BaseEntity
from delpinos.crud.core.domain.entities.filter_entity import FilterEntity
from delpinos.crud.core.domain.entities.pagination_entity import PaginationEntity
from delpinos.crud.core.domain.entities.sort_field_entity import SortFieldEntity
from delpinos.crud.core.application.repositories.base_repository import BaseRepository
from sqlalchemy_filters import apply_filters, apply_sort
from sqlalchemy.orm import Query, Session
from delpinos.crud.sqlalchemy.application.encoders.sqlalchemy_encoder import (
    SqlAlchemyEncoder,
)

from delpinos.crud.sqlalchemy.application.models.sqlalchemy_model import SqlAlchemyModel
from delpinos.crud.sqlalchemy.connection import SqlAlchemyConnection


class SqlAlchemyRepository(BaseRepository):
    def add_factories(self):
        super().add_factories()
        SqlAlchemyEncoder.add_factories_encoders(self)
        self.add_factory_impl("sqlalchemy.connection", SqlAlchemyConnection)
        self.add_factory(
            "sqlalchemy.session",
            lambda _: self.sqlalchemy_connection.new_session(),
        )

    @property
    def sqlalchemy_connection(self) -> SqlAlchemyConnection:
        return self.instance(
            "sqlalchemy.connection",
            SqlAlchemyConnection,
        )

    @property
    def encoder(self) -> EncoderAbstract:
        return self.instance("encoders.sqlalchemy", SqlAlchemyEncoder)

    @property
    def model(self) -> Type[SqlAlchemyModel]:
        raise NotImplementedError()

    @property
    def model_view(self) -> Type[SqlAlchemyModel]:
        return self.model

    @property
    def session(self) -> Session:
        return self.instance("sqlalchemy.session", Session)

    def build_query(self, model: type[SqlAlchemyModel]) -> Query:
        return self.session.query(model)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def build_entity(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        if isinstance(values, SqlAlchemyModel):
            values = values.model_dump(by_alias=True)
        return super().build_entity(values)

    def build_entity_view(
        self,
        values: Dict[str, Any] | BaseEntity,
    ) -> BaseEntity:
        if isinstance(values, SqlAlchemyModel):
            values = values.model_dump(by_alias=True)
        return super().build_entity_view(values)

    def filter_query(
        self,
        query: Query,
        filter_entity: FilterEntity | None = None,
    ):
        if query and isinstance(filter_entity, FilterEntity):
            filter_dict = filter_entity.model_dump(
                by_alias=True, exclude_none=True, exclude_unset=True
            )
            if filter_dict:
                return apply_filters(query, filter_dict)
        return query

    def sorting_query(
        self,
        query: Query,
        sorting: List[SortFieldEntity] | None = None,
    ):
        if query and isinstance(sorting, list):
            sorting_list = [
                sort.model_dump(by_alias=True)
                for sort in sorting
                if isinstance(sort, SortFieldEntity)
            ]
            if sorting_list:
                return apply_sort(query, sorting_list)
        return query

    def pagination_query(
        self,
        query: Query,
        pagination: PaginationEntity | None = None,
    ):
        if query and isinstance(pagination, PaginationEntity):
            if pagination.limit:
                query = query.limit(pagination.limit)
            if pagination.offset:
                query = query.offset(pagination.offset)
        return query

    def prepare_query(
        self,
        query: Query,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ):
        if query:
            query = self.filter_query(query, filter_entity)
            query = self.sorting_query(query, sorting)
            query = self.pagination_query(query, pagination)
        # self.debug_query(query)
        return query

    def debug_query(self, query: Query):
        # query_as_string = query.statement.compile(
        #    compile_kwargs={"literal_binds": True}
        # )
        # self.logger.debug(query_as_string)
        return query

    def find_query(
        self,
        query: Query,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ):
        return self.prepare_query(query, filter_entity, sorting, pagination)

    def count_query(
        self,
        query: Query,
        filter_entity: FilterEntity | None = None,
    ):
        return self.filter_query(query, filter_entity)

    def find(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        query = self.find_query(
            self.build_query(self.model),
            filter_entity,
            sorting,
            pagination,
        )
        return list(
            map(self.build_entity, query.all() or []),
        )

    def find_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
        pagination: PaginationEntity | None = None,
    ) -> List[BaseEntity]:
        query = self.find_query(
            self.build_query(self.model_view),
            filter_entity,
            sorting,
            pagination,
        )
        return list(
            map(self.build_entity_view, query.all() or []),
        )

    def find_one(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        query = self.find_query(
            self.build_query(self.model),
            filter_entity,
            sorting,
            PaginationEntity(limit=1),
        )
        data = query.first()
        if isinstance(data, SqlAlchemyModel):
            data = data.model_dump(by_alias=True)
            return self.build_entity(data)
        return None

    def find_one_view(
        self,
        filter_entity: FilterEntity | None = None,
        sorting: List[SortFieldEntity] | None = None,
    ) -> BaseEntity | None:
        query = self.find_query(
            self.build_query(self.model_view),
            filter_entity,
            sorting,
            PaginationEntity(limit=1),
        )
        data = query.first()
        if isinstance(data, SqlAlchemyModel):
            data = data.model_dump(by_alias=True)
            return self.build_entity_view(data)
        return None

    def count(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        return self.count_query(
            self.build_query(self.model),
            filter_entity,
        ).count()

    def count_view(
        self,
        filter_entity: FilterEntity | None = None,
    ) -> int:
        return self.count_query(
            self.build_query(self.model_view),
            filter_entity,
        ).count()

    def insert(self, values: BaseEntity) -> BaseEntity:
        if not isinstance(values, BaseEntity):
            raise BadRequestException()
        obj_model = self.model(**values.model_dump(by_alias=True))
        if isinstance(obj_model, SqlAlchemyModel):
            self.session.add(obj_model)
        return self.build_entity(values)

    def update(self, filter_entity: FilterEntity, values: BaseEntity) -> BaseEntity:
        query = self.build_query(self.model)
        query = self.filter_query(query, filter_entity)
        obj_model = query.first()
        if isinstance(obj_model, SqlAlchemyModel):
            obj_model.merge(values)
            return self.build_entity(
                obj_model.model_dump(by_alias=True),
            )
        raise NotFoundException()

    def delete(self, filter_entity: FilterEntity) -> BaseEntity:
        query = self.build_query(self.model)
        query = self.filter_query(query, filter_entity)
        obj_model = query.first()
        if isinstance(obj_model, SqlAlchemyModel):
            self.session.delete(obj_model)
            return self.build_entity(
                obj_model.model_dump(by_alias=True),
            )
        raise NotFoundException()
