import sqlite3
import re
import time
from typing import Dict, Any, List, Optional, Tuple

FORBIDDEN_SQL_KEYWORDS = [
    r"\bINSERT\b", r"\bUPDATE\b", r"\bDELETE\b", r"\bDROP\b",
    r"\bALTER\b", r"\bCREATE\b", r"\bATTACH\b", r"\bDETACH\b",
    r"\bPRAGMA\b", r"\bREPLACE\b", r"\bTRUNCATE\b", r"\bGRANT\b", r"\bREVOKE\b"
]

SAMPLE_SCHEMA_DDL = """
-- Department & Employee Schema
CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    dept_name TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    dept_id INTEGER,
    salary REAL NOT NULL,
    hire_date DATE NOT NULL,
    role TEXT NOT NULL,
    FOREIGN KEY(dept_id) REFERENCES departments(dept_id)
);

-- Students & Academics Schema
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    major TEXT NOT NULL,
    gpa REAL NOT NULL,
    graduation_year INTEGER NOT NULL
);

CREATE TABLE courses (
    course_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    credits INTEGER NOT NULL,
    department TEXT NOT NULL
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id TEXT,
    grade TEXT NOT NULL,
    score REAL NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

-- Orders & E-Commerce Schema
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    order_date DATE NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL
);
"""

SAMPLE_DATA_SEED = """
-- Departments
INSERT INTO departments (dept_id, dept_name, location) VALUES
(1, 'Engineering', 'Building A'),
(2, 'Data Science', 'Building B'),
(3, 'Product Management', 'Building A'),
(4, 'Human Resources', 'Building C');

-- Employees
INSERT INTO employees (emp_id, first_name, last_name, dept_id, salary, hire_date, role) VALUES
(101, 'Adhithian', 'S', 2, 95000, '2023-06-15', 'AI Engineer'),
(102, 'Priya', 'Raman', 1, 88000, '2022-03-10', 'Backend Developer'),
(103, 'Karthik', 'Nair', 1, 105000, '2021-08-01', 'Senior Architect'),
(104, 'Ananya', 'Sharma', 3, 92000, '2023-01-20', 'Product Specialist'),
(105, 'Vikram', 'Patel', 2, 75000, '2024-02-15', 'Junior Data Analyst'),
(106, 'Deepa', 'Iyer', 4, 68000, '2022-11-05', 'HR Executive'),
(107, 'Rahul', 'Verma', 1, 98000, '2022-07-18', 'DevOps Specialist');

-- Students
INSERT INTO students (student_id, name, major, gpa, graduation_year) VALUES
(1, 'Arun Kumar', 'AI and Data Science', 8.85, 2027),
(2, 'Divya Prakash', 'Computer Science', 9.10, 2026),
(3, 'Rohit Menon', 'AI and Data Science', 7.90, 2027),
(4, 'Meera Joshi', 'Information Technology', 8.40, 2026),
(5, 'Siddharth Rao', 'AI and Data Science', 9.40, 2027);

-- Courses
INSERT INTO courses (course_id, title, credits, department) VALUES
('CS101', 'Data Structures & Algorithms', 4, 'Computer Science'),
('AI201', 'Machine Learning Fundamentals', 4, 'AI and Data Science'),
('DB301', 'Database Management Systems', 3, 'Computer Science'),
('NW101', 'Computer Networks', 3, 'Information Technology');

-- Enrollments
INSERT INTO enrollments (enrollment_id, student_id, course_id, grade, score) VALUES
(1, 1, 'CS101', 'A', 92.5),
(2, 1, 'AI201', 'S', 96.0),
(3, 1, 'DB301', 'A', 89.0),
(4, 2, 'CS101', 'S', 98.0),
(5, 2, 'NW101', 'A', 91.0),
(6, 3, 'CS101', 'B', 78.5),
(7, 3, 'DB301', 'B', 81.0),
(8, 4, 'NW101', 'A', 88.0),
(9, 5, 'AI201', 'S', 99.0),
(10, 5, 'CS101', 'S', 95.0);

-- Orders
INSERT INTO orders (order_id, customer_name, order_date, total_amount, status) VALUES
(501, 'Alpha Corp', '2026-01-10', 4500.00, 'Completed'),
(502, 'Beta Tech', '2026-01-15', 1200.50, 'Completed'),
(503, 'Gamma Labs', '2026-02-01', 8900.00, 'Processing'),
(504, 'Delta Solutions', '2026-02-14', 320.00, 'Completed'),
(505, 'Epsilon Systems', '2026-03-01', 6700.25, 'Shipped');
"""

def create_sandbox_connection() -> sqlite3.Connection:
    """Creates an in-memory SQLite database populated with the sample schema and seed data."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.executescript(SAMPLE_SCHEMA_DDL)
    cursor.executescript(SAMPLE_DATA_SEED)
    conn.commit()
    return conn

def validate_sql_query(query: str) -> Optional[str]:
    """Ensures query is strictly a read-only SELECT statement."""
    trimmed = query.strip()
    if not trimmed:
        return "Query cannot be empty."
    
    # Must start with SELECT or WITH (for CTEs)
    if not re.match(r"^(SELECT|WITH)\b", trimmed, re.IGNORECASE):
        return "Only SELECT or WITH (CTE) queries are permitted for safety and practice."
    
    for pattern in FORBIDDEN_SQL_KEYWORDS:
        if re.search(pattern, trimmed, re.IGNORECASE):
            return f"Prohibited SQL keyword detected. Non-SELECT operations are blocked."
            
    return None

def normalize_row(row: Any) -> tuple:
    """Normalizes row values (e.g. floats rounded, strings stripped) for consistent comparison."""
    norm = []
    for val in row:
        if isinstance(val, float):
            norm.append(round(val, 2))
        elif isinstance(val, str):
            norm.append(val.strip())
        else:
            norm.append(val)
    return tuple(norm)

def execute_sql_practice(
    user_query: str,
    expected_query: str,
    max_rows: int = 100
) -> Dict[str, Any]:
    """
    Executes learner query against an isolated SQLite sandbox and compares with expected solution query.
    """
    validation_err = validate_sql_query(user_query)
    if validation_err:
        return {
            "passed": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "execution_time_ms": 0.0,
            "error": validation_err
        }

    conn = create_sandbox_connection()
    try:
        cursor = conn.cursor()
        
        # 1. Run expected query to obtain ground truth
        cursor.execute(expected_query)
        expected_cols = [desc[0].lower() for desc in cursor.description] if cursor.description else []
        expected_raw_rows = cursor.fetchall()
        expected_rows = [list(r) for r in expected_raw_rows]
        normalized_expected = sorted([normalize_row(r) for r in expected_raw_rows])

        # 2. Run learner query with timing
        start_time = time.time()
        cursor.execute(user_query)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        
        user_cols = [desc[0].lower() for desc in cursor.description] if cursor.description else []
        user_raw_rows = cursor.fetchmany(max_rows)
        user_rows = [list(r) for r in user_raw_rows]
        normalized_user = sorted([normalize_row(r) for r in user_raw_rows])

        # 3. Check column count and row equivalence
        col_count_match = len(user_cols) == len(expected_cols)
        row_match = (normalized_user == normalized_expected)
        passed = col_count_match and row_match

        error_msg = None
        if not passed:
            if not col_count_match:
                error_msg = f"Column count mismatch: Query returned {len(user_cols)} columns, expected {len(expected_cols)}."
            elif len(normalized_user) != len(normalized_expected):
                error_msg = f"Row count mismatch: Returned {len(normalized_user)} rows, expected {len(normalized_expected)} rows."
            else:
                error_msg = "Data mismatch: Result rows did not match expected values. Check filtering (WHERE), joins, or GROUP BY aggregations."

        return {
            "passed": passed,
            "columns": user_cols,
            "rows": user_rows,
            "row_count": len(user_rows),
            "execution_time_ms": elapsed_ms,
            "error": error_msg,
            "expected_rows_sample": expected_rows[:5] if not passed else None
        }

    except sqlite3.Error as e:
        return {
            "passed": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "execution_time_ms": 0.0,
            "error": f"SQL Syntax/Execution Error: {str(e)}"
        }
    finally:
        conn.close()
