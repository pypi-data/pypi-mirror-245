# coding: utf-8

"""
    Lidarr

    Lidarr API docs  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import annotations
from inspect import getfullargspec
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, ClassVar, Dict, Optional
from pydantic import BaseModel

class LogResource(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    id: Optional[int]
    time: Optional[datetime]
    exception: Optional[str]
    exception_type: Optional[str]
    level: Optional[str]
    logger: Optional[str]
    message: Optional[str]
    method: Optional[str]
    __properties = ["id", "time", "exception", "exceptionType", "level", "logger", "message", "method"]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        alias_generator = lambda x: x.split("_")[0] + "".join(word.capitalize() for word in x.split("_")[1:])

    def __getitem__(self, item):
        return getattr(self, item)

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LogResource:
        """Create an instance of LogResource from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if exception (nullable) is None
        if self.exception is None:
            _dict['exception'] = None

        # set to None if exception_type (nullable) is None
        if self.exception_type is None:
            _dict['exceptionType'] = None

        # set to None if level (nullable) is None
        if self.level is None:
            _dict['level'] = None

        # set to None if logger (nullable) is None
        if self.logger is None:
            _dict['logger'] = None

        # set to None if message (nullable) is None
        if self.message is None:
            _dict['message'] = None

        # set to None if method (nullable) is None
        if self.method is None:
            _dict['method'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LogResource:
        """Create an instance of LogResource from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return LogResource.parse_obj(obj)

        _obj = LogResource.parse_obj({
            "id": obj.get("id"),
            "time": obj.get("time"),
            "exception": obj.get("exception"),
            "exception_type": obj.get("exceptionType"),
            "level": obj.get("level"),
            "logger": obj.get("logger"),
            "message": obj.get("message"),
            "method": obj.get("method")
        })
        return _obj

