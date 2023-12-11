from __future__ import annotations

from typing import ClassVar, List

from hojo.orm.manager import Manager, ModelDescriptor
from hojo.schema import BaseSchema


class BaseModel(BaseSchema):
    _registry: List[BaseModel] = []

    objects: ClassVar = ModelDescriptor(Manager())

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry.append(cls)
