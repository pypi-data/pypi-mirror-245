"""
There are good reasons the package has separate schemas from the rest of the app
1. We don't necessarily want to expose the underlying schema
2. The package requires quite different objects - notably all input parameters need to be defined in the app parameter
"""
from typing import List, Union, Any, Optional
from pydantic import BaseModel, validator, Field

from uuid import UUID

# import json_fix
# from uuid import UUID as NativeUUID
# class UUID(NativeUUID):
#     def __init__(self, uuid_string):
#         super().__init__(uuid_string)
        
#     def __json__(self):
#         return str(self)

class CaseTrigger(BaseModel):
    case_id: UUID
    vars: dict


class RunTrigger(BaseModel):
    run_id: UUID
    cases: List[CaseTrigger]

    
class PollResponse(BaseModel):
    registered_apps: List[UUID]
    run_trigger: Optional[RunTrigger] = None
    

class AppDeletionEvent(BaseModel):
    type: str = Field(default="app_deletion")
        

class CaseResult(BaseModel):
    case_id: UUID
    value: Any = None
    error: Optional[str] = None
    

class RunResult(BaseModel):
    run_id: UUID
    results: Optional[List[CaseResult]] = None
    error: Optional[str] = None

class AppRegistration(BaseModel):
    api_key: str
    parameters: List[str]
    types: List[str]  # This needs to be a string because you can't send the frontend a 'type'
    demo_values: List[Union[int, float, str]]
    descriptions: List[Optional[str]]
    constraints: List[Optional[str]]
