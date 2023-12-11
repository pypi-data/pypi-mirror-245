from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Tuple, Type, TypeVar, Union

from sqlalchemy import delete, select, update
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.orm import Session

T = TypeVar("T")


@dataclass
class LookupFilter:
    field_name: str
    lookup: str
    value: Any
    exclude: bool


class QuerySet:
    def __init__(self, model_class: Type[T], session: Session) -> None:
        self.model_class = model_class
        self.session = session
        self.query = select(model_class)
        self._result_cache = None
        self._executed = False
        self.lookup_filters: List[LookupFilter] = []

    def __iter__(self):
        if not self._executed:
            self._select()
        return iter(self._result_cache)

    def __len__(self):
        if not self._executed:
            self._select()
        return len(self._result_cache)

    def __bool__(self):
        if not self._executed:
            self._select()
        return bool(self._result_cache)

    def __repr__(self):
        if not self._executed:
            return "<QuerySet [not executed]>"
        return repr(self._result_cache)

    def _clone(self) -> QuerySet[T]:
        qs = self.__class__(self.model_class, self.session)
        qs.query = self.query
        qs.lookup_filters = self.lookup_filters.copy()
        return qs

    def compile_conditions(self):
        if self.lookup_filters:
            conditions = []
            for lookup in self.lookup_filters:
                column = getattr(self.model_class, lookup.field_name)
                lookup_name = lookup.lookup
                if lookup_name == "eq":
                    filter_expr = column == lookup.value
                elif lookup_name == "gt":
                    filter_expr = column > lookup.value
                elif lookup_name == "gte":
                    filter_expr = column >= lookup.value
                elif lookup_name == "lt":
                    filter_expr = column < lookup.value
                elif lookup_name == "lte":
                    filter_expr = column <= lookup.value
                elif lookup_name == "in":
                    filter_expr = column.in_(lookup.value)
                elif lookup_name == "isnull":
                    filter_expr = column.is_(None)
                elif lookup_name == "between":
                    filter_expr = column.between(*lookup.value)
                else:
                    filter_expr = getattr(column, lookup_name)(lookup.value)
                if lookup.exclude:
                    filter_expr = ~filter_expr
                conditions.append(filter_expr)

            return conditions

    def _mount_filters(self):
        conditions = self.compile_conditions()
        self.query = self.query.where(*conditions)

    def _select(self):
        self._mount_filters()

        print(self.query)

        self._result_cache = self.session.execute(self.query).scalars().all()
        self._executed = True

    def _apply_filter(self, exclude=False, **kwargs) -> QuerySet[T]:
        cloned_qs = self._clone()

        lookups = [
            "like",
            "ilike",
            "contains",
            "startswith",
            "endswith",
            "gt",
            "lt",
            "gte",
            "lte",
            "isnull",
            "in",
            "between",
        ]

        for key, val in kwargs.items():
            parts = key.split("__")
            field_name = parts[0]
            if len(parts) > 1:
                lookup = parts[1]
                if lookup not in lookups:
                    raise ValueError(f"Unsupported lookup filter: {lookup}")
            else:
                lookup = "eq"

            cloned_qs.lookup_filters.append(
                LookupFilter(field_name, lookup, val, exclude)
            )

        return cloned_qs

    def all(self) -> QuerySet[T]:
        return self._clone()

    def first(self) -> Union[T, None]:
        if not self._executed:
            self._select()
        return self._result_cache[0] if self._result_cache else None

    def last(self) -> Union[T, None]:
        if not self._executed:
            self._select()
        return self._result_cache[-1] if self._result_cache else None

    def order_by(self, *fields: str) -> QuerySet[T]:
        cloned_qs = self._clone()
        for field in fields:
            cloned_qs.query = cloned_qs.query.order_by(getattr(self.model_class, field))
        return cloned_qs

    def filter(self, **kwargs) -> QuerySet[T]:
        return self._apply_filter(**kwargs)

    def exclude(self, **kwargs) -> QuerySet[T]:
        return self._apply_filter(exclude=True, **kwargs)

    def create(self, **kwargs) -> T:
        obj = self.model_class.load(kwargs)
        self.session.add(obj)
        self.session.commit()
        return obj

    def delete(self, **kwargs) -> None:
        conditions = self.compile_conditions()
        delete_query = delete(self.model_class).where(*conditions)

        self.session.execute(delete_query)
        self.session.commit()

    def update(self, **kwargs) -> None:
        conditions = self.compile_conditions()
        update_query = update(self.model_class).where(*conditions).values(**kwargs)

        self.session.execute(update_query)
        self.session.commit()

    def get(self, **kwargs) -> T:
        try:
            return self.filter(**kwargs).first()
        except NoResultFound:
            raise ValueError("No results found.")
        except MultipleResultsFound:
            raise ValueError("Multiple results returned for `get`.")
