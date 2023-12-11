"""
There are good reasons the package has separate schemas from the rest of the app
1. We don't necessarily want to expose the underlying schema
2. The package requires quite different objects - notably all input parameters need to be defined in the app parameter
"""

from typing import List, Union, Any, Optional, Literal
from pydantic import BaseModel, Field
import uuid

class CaseTrigger(BaseModel):
    case_id: uuid.UUID
    vars: dict

    class Config:
        schema_extra = {
            "examples": [
                {
                    "case_id": uuid.uuid4(),
                    "vars": {"param1": 1, "param2": "test"},
                }
            ]
        }


class RunTrigger(BaseModel):
    run_id: uuid.UUID
    cases: List[CaseTrigger]
    
class AppDeletionEvent(BaseModel):
    type: str = Field(default="app_deletion")
    message: str


class PollResponse(BaseModel):
    registered_apps: List[uuid.UUID]
    payload: Union[None, RunTrigger, AppDeletionEvent] = None


class CaseResult(BaseModel):
    case_id: uuid.UUID
    value: Any = None
    error: Optional[str] = None

    class Config:
        schema_extra = {
            "examples": [
                {
                    "value": "Output value of the linked app",
                    "error": None,
                }
            ]
        }


class RunResult(BaseModel):
    run_id: uuid.UUID
    results: Optional[List[CaseResult]] = None
    error: Optional[str] = None

    class Config:
        schema_extra = {
            "examples": [
                {
                    "run_id": uuid.uuid4(),
                    "results": [
                        {
                            "case_id": uuid.uuid4(),
                            "value": "Output value provided if error is null",
                            "error": None,
                        },
                        {
                            "case_id": uuid.uuid4(),
                            "value": None,
                            "error": "Error message provided if value is null",
                        },
                    ],
                    "error": "A run error: should only be set if the run itself fails, not if a case fails",
                }
            ]
        }


class AppRegistration(BaseModel):
    api_key: str
    runner_type: Literal["python", "golang"]
    runner_version: str
    parameters: List[str]
    types: List[
        str
    ]  # This needs to be a string because you can't send the frontend a 'type'
    demo_values: List[Union[int, float, str]]
    descriptions: List[Optional[str]]
    constraints: List[Optional[str]]

    class Config:
        schema_extra = {
            "examples": [
                {
                    "api_key": "cp-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "parameters": ["param1", "param2"],
                    "types": ["int", "str"],
                    "demo_values": [1, "test"],
                    "descriptions": ["this is param 1", None],
                    "constraints": ["greater than 0 but less than 2", None],
                }
            ]
        }
