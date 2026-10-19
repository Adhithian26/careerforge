from backend.app.services.sql_sandbox import execute_sql_practice, validate_sql_query

def test_sql_forbidden_keyword_protection():
    # DROP TABLE query
    drop_query = "DROP TABLE employees;"
    err = validate_sql_query(drop_query)
    assert err is not None
    assert "Only SELECT" in err or "Prohibited" in err

    # INSERT query
    insert_query = "INSERT INTO employees VALUES (999, 'Hacker', 'X', 1, 99999, '2026-01-01', 'Admin');"
    err2 = validate_sql_query(insert_query)
    assert err2 is not None

def test_sql_practice_execution_success():
    user_query = "SELECT first_name, last_name, salary FROM employees WHERE dept_id = 1 ORDER BY salary DESC;"
    expected_query = "SELECT first_name, last_name, salary FROM employees WHERE dept_id = 1 ORDER BY salary DESC;"
    
    res = execute_sql_practice(user_query, expected_query)
    assert res["passed"] is True
    assert res["row_count"] > 0
    assert len(res["columns"]) == 3
    assert res["error"] is None

def test_sql_mismatch_handling():
    # Intentionally missing one column
    user_query = "SELECT first_name, salary FROM employees WHERE dept_id = 1;"
    expected_query = "SELECT first_name, last_name, salary FROM employees WHERE dept_id = 1;"
    
    res = execute_sql_practice(user_query, expected_query)
    assert res["passed"] is False
    assert "mismatch" in res["error"].lower()
