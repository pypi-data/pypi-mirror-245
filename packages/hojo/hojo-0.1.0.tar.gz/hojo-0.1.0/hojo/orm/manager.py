from __future__ import annotations

from typing import Any, Optional, TypeVar

from hojo.connection import Connection
from hojo.orm.queryset import QuerySet
from hojo.schema import BaseSchema

T = TypeVar("T")


class Manager:
    """
    Interface for database operations that provides a high-level, abstracted set of
    database-querying methods.
    """

    def __init__(self) -> None:
        self._model_class: Optional[type[T]] = None

    @property
    def model_class(self) -> type[T]:
        if self._model_class is None:
            raise ValueError("Model class is not set for this manager.")
        return self._model_class

    @model_class.setter
    def model_class(self, value: type[T]) -> None:
        self._model_class = value

    def get_queryset(self) -> QuerySet[T]:
        return QuerySet(self._model_class, Connection().session)

    def all(self) -> QuerySet[T]:
        return self.get_queryset().all()

    def filter(self, **kwargs) -> QuerySet[T]:
        return self.get_queryset().filter(**kwargs)

    def exclude(self, **kwargs) -> QuerySet[T]:
        return self.get_queryset().exclude(**kwargs)

    def first(self) -> T:
        return self.get_queryset().first()

    def last(self) -> T:
        return self.get_queryset().last()

    def create(self, data: dict | BaseSchema) -> T:
        if isinstance(data, BaseSchema):
            data = data.dump()

        return self.get_queryset().create(**data)

    def get(self, **kwargs) -> T:
        return self.get_queryset().get(**kwargs)

    def get_or_create(self, **kwargs) -> T:
        return self.get_queryset().get_or_create(**kwargs)

    def bulk_create(self, objs):
        return self.get_queryset().bulk_create(objs)

    def bulk_update(self, objs):
        return self.get_queryset().bulk_update(objs)

    def count(self) -> int:
        return self.get_queryset().count()

    def order_by(self, *fields: str) -> QuerySet[T]:
        return self.get_queryset().order_by(*fields)

    def values(self, *fields: str) -> list[dict]:
        return self.get_queryset().values(*fields)

    def values_list(self, *fields: str, flat=False) -> list:
        return self.get_queryset().values_list(*fields, flat=flat)

    def exists(self) -> bool:
        return self.get_queryset().exists()

    def delete(self) -> None:
        self.get_queryset().delete()

    def update(self, **kwargs) -> None:
        self.get_queryset().update(**kwargs)

    def annotate(self, **kwargs) -> QuerySet[T]:
        return self.get_queryset().annotate(**kwargs)

    def aggregate(self, **kwargs) -> dict:
        return self.get_queryset().aggregate(**kwargs)

    def reverse(self) -> QuerySet[T]:
        return self.get_queryset().reverse()

    def distinct(self) -> QuerySet[T]:
        return self.get_queryset().distinct()


class ModelDescriptor:
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError("Manager isn't accessible via model instances")

        # Bind the model class to the manager and return it
        self.manager.model_class = owner
        return self.manager
