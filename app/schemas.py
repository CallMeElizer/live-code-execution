from pydantic import BaseModel
from typing import Optional

class CodeUpdate(BaseModel):
    language: str
    source_code: str

class ExecutionResponse(BaseModel):
    session_id: Optional[str] = None
    execution_id: Optional[str] = None
    status: str

class ExecutionResult(BaseModel):
    execution_id: str
    status: str
    stdout: Optional[str] = ""
    stderr: Optional[str] = ""
    execution_time_ms: Optional[int] = 0