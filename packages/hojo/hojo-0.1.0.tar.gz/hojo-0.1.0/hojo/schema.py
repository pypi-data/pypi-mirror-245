from __future__ import annotations

from dataclasses import field
from typing import Dict, Union

from marshmallow.utils import EXCLUDE
from marshmallow_dataclass import dataclass
from uuid6 import UUID
from uuid6 import uuid7 as uuid7


class BaseSchema:
    @classmethod
    def load(cls, data: Union[dict, BaseSchema], unknown=EXCLUDE, **kwargs):
        if isinstance(data, BaseSchema):
            data = data.dump()

        return cls.Schema().load(data, unknown=unknown, **kwargs)

    def dump(self, skip_none=False, **kwargs):
        data = self.Schema(**kwargs).dump(self)

        if skip_none:
            data = {key: val for key, val in data.items() if val is not None}

        return data
