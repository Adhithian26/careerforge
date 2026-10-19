from typing import List, Optional, Any, Dict
from datetime import datetime
from pydantic import BaseModel

class CodingProblemSummary(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    category: str

    class Config:
        from_attributes = True

class CodingProblemDetail(CodingProblemSummary):
    description: str
    starter_code: str
    function_name: str
    hints: List[str]
    sample_tests: List[Dict[str, Any]]

class CodingRunRequest(BaseModel):
    code: str

class CodingSubmitRequest(BaseModel):
    code: str

class TestResultItem(BaseModel):
    test_index: int
    passed: bool
    input_str: Optional[str] = None
    expected_str: Optional[str] = None
    actual_str: Optional[str] = None
    error: Optional[str] = None

class CodingExecutionResponse(BaseModel):
    passed: bool
    passed_tests: int
    total_tests: int
    runtime_ms: float
    output: Optional[str] = None
    error: Optional[str] = None
    results: List[TestResultItem]
    solution_approach: Optional[str] = None

class SqlProblemSummary(BaseModel):
    id: str
    slug: str
    title: str
    difficulty: str
    category: str

    class Config:
        from_attributes = True

class SqlProblemDetail(SqlProblemSummary):
    prompt: str
    schema_info: str
    hints: List[str]

class SqlExecuteRequest(BaseModel):
    query: str

class SqlExecutionResponse(BaseModel):
    passed: bool
    columns: List[str] = []
    rows: List[List[Any]] = []
    row_count: int = 0
    execution_time_ms: float = 0.0
    error: Optional[str] = None
    expected_rows_sample: Optional[List[List[Any]]] = None
    explanation: Optional[str] = None
