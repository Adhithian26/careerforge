from backend.app.services.code_executor import execute_coding_exercise, validate_code_safety

def test_ast_security_blocking():
    # Attempting to import os
    unsafe_code = "import os\ndef two_sum(nums, target):\n    return [0, 1]"
    errors = validate_code_safety(unsafe_code)
    assert len(errors) > 0
    assert "os" in errors[0]

    # Attempting to use open()
    unsafe_code2 = "def two_sum(nums, target):\n    f = open('secret.txt', 'r')\n    return [0, 1]"
    errors2 = validate_code_safety(unsafe_code2)
    assert len(errors2) > 0
    assert "open" in errors2[0]

def test_correct_two_sum_execution():
    user_code = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
"""
    test_cases = [
        {"input": [[2, 7, 11, 15], 9], "expected": [0, 1], "is_sample": True},
        {"input": [[3, 2, 4], 6], "expected": [1, 2], "is_sample": False}
    ]
    res = execute_coding_exercise(user_code, "two_sum", test_cases)
    assert res["passed"] is True
    assert res["passed_tests"] == 2
    assert res["total_tests"] == 2
    assert res["runtime_ms"] > 0

def test_failed_test_case_safeguard():
    # Code that returns wrong answer for second test case
    user_code = """
def two_sum(nums, target):
    return [0, 1]
"""
    test_cases = [
        {"input": [[2, 7, 11, 15], 9], "expected": [0, 1], "is_sample": True},
        {"input": [[3, 2, 4], 6], "expected": [1, 2], "is_sample": False}
    ]
    res = execute_coding_exercise(user_code, "two_sum", test_cases)
    assert res["passed"] is False
    assert res["passed_tests"] == 1
    # Check that hidden test case input/output was NOT leaked
    hidden_result = res["results"][1]
    assert hidden_result["passed"] is False
    assert hidden_result["input_str"] == "[Hidden test case]"
    assert hidden_result["expected_str"] == "[Hidden test case]"

def test_timeout_protection():
    infinite_loop_code = """
def two_sum(nums, target):
    while True:
        pass
"""
    test_cases = [{"input": [[1, 2], 3], "expected": [0, 1], "is_sample": True}]
    res = execute_coding_exercise(infinite_loop_code, "two_sum", test_cases, timeout_seconds=1.0)
    assert res["passed"] is False
    assert "Time Limit Exceeded" in res["error"]
