# coding: utf-8

"""
    FINBOURNE Luminesce Web API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, conlist
from luminesce.models.background_query_state import BackgroundQueryState
from luminesce.models.column import Column
from luminesce.models.feedback_event_args import FeedbackEventArgs
from luminesce.models.task_status import TaskStatus

class BackgroundQueryProgressResponse(BaseModel):
    """
    BackgroundQueryProgressResponse
    """
    has_data: Optional[StrictBool] = Field(None, alias="hasData", description="Is there currently data for this Query?")
    row_count: Optional[StrictInt] = Field(None, alias="rowCount", description="Number of rows of data held. -1 if none as yet.")
    status: Optional[TaskStatus] = None
    state: Optional[BackgroundQueryState] = None
    progress: Optional[StrictStr] = Field(None, description="The full progress log (up to this point at least)")
    feedback: Optional[conlist(FeedbackEventArgs)] = Field(None, description="Individual Feedback Messages (to replace Progress).  A given message will be returned from only one call.")
    query: Optional[StrictStr] = Field(None, description="The LuminesceSql of the original request")
    query_name: Optional[StrictStr] = Field(None, alias="queryName", description="The QueryName given in the original request")
    columns_available: Optional[conlist(Column)] = Field(None, alias="columnsAvailable", description="When HasData is true this is the schema of columns that will be returned if the data is requested")
    __properties = ["hasData", "rowCount", "status", "state", "progress", "feedback", "query", "queryName", "columnsAvailable"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BackgroundQueryProgressResponse:
        """Create an instance of BackgroundQueryProgressResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in feedback (list)
        _items = []
        if self.feedback:
            for _item in self.feedback:
                if _item:
                    _items.append(_item.to_dict())
            _dict['feedback'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in columns_available (list)
        _items = []
        if self.columns_available:
            for _item in self.columns_available:
                if _item:
                    _items.append(_item.to_dict())
            _dict['columnsAvailable'] = _items
        # set to None if progress (nullable) is None
        # and __fields_set__ contains the field
        if self.progress is None and "progress" in self.__fields_set__:
            _dict['progress'] = None

        # set to None if feedback (nullable) is None
        # and __fields_set__ contains the field
        if self.feedback is None and "feedback" in self.__fields_set__:
            _dict['feedback'] = None

        # set to None if query (nullable) is None
        # and __fields_set__ contains the field
        if self.query is None and "query" in self.__fields_set__:
            _dict['query'] = None

        # set to None if query_name (nullable) is None
        # and __fields_set__ contains the field
        if self.query_name is None and "query_name" in self.__fields_set__:
            _dict['queryName'] = None

        # set to None if columns_available (nullable) is None
        # and __fields_set__ contains the field
        if self.columns_available is None and "columns_available" in self.__fields_set__:
            _dict['columnsAvailable'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BackgroundQueryProgressResponse:
        """Create an instance of BackgroundQueryProgressResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BackgroundQueryProgressResponse.parse_obj(obj)

        _obj = BackgroundQueryProgressResponse.parse_obj({
            "has_data": obj.get("hasData"),
            "row_count": obj.get("rowCount"),
            "status": obj.get("status"),
            "state": obj.get("state"),
            "progress": obj.get("progress"),
            "feedback": [FeedbackEventArgs.from_dict(_item) for _item in obj.get("feedback")] if obj.get("feedback") is not None else None,
            "query": obj.get("query"),
            "query_name": obj.get("queryName"),
            "columns_available": [Column.from_dict(_item) for _item in obj.get("columnsAvailable")] if obj.get("columnsAvailable") is not None else None
        })
        return _obj
