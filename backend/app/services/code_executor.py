import ast
import json
import subprocess
import sys
import tempfile
import time
from typing import List, Dict, Any, Tuple

# Restricted AST node visitor to block unsafe operations
FORBIDDEN_MODULES = {
    "os", "sys", "subprocess", "socket", "shutil", "urllib", "requests", "http",
    "posix", "nt", "importlib", "pathlib", "ctypes", "multiprocessing", "threading", "signal"
}

FORBIDDEN_BUILTINS = {
    "open", "eval", "exec", "compile", "__import__", "breakpoint", "memoryview", "globals", "locals"
}

FORBIDDEN_ATTRIBUTES = {
    "__subclasses__", "__globals__", "__code__", "__closure__", "__bases__", "__class__"
}

class CodeSecurityValidator(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            base_module = alias.name.split(".")[0]
            if base_module in FORBIDDEN_MODULES:
                self.errors.append(f"Security Policy: Module import '{alias.name}' is prohibited in coding exercises.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            base_module = node.module.split(".")[0]
            if base_module in FORBIDDEN_MODULES:
                self.errors.append(f"Security Policy: Module import from '{node.module}' is prohibited in coding exercises.")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_BUILTINS:
                self.errors.append(f"Security Policy: Use of builtin function '{node.func.id}' is prohibited.")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if node.attr in FORBIDDEN_ATTRIBUTES:
            self.errors.append(f"Security Policy: Access to internal attribute '{node.attr}' is prohibited.")
        self.generic_visit(node)

def validate_code_safety(code: str) -> List[str]:
    """Parses code AST and enforces security rules."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [f"Syntax Error: {e.msg} on line {e.lineno}"]
    
    validator = CodeSecurityValidator()
    validator.visit(tree)
    return validator.errors

HARNESS_TEMPLATE = """# Restricted Test Runner Harness
import json
import sys

# User Code
{user_code}

def main():
    test_cases = json.loads('''{test_cases_json}''')
    func_name = "{function_name}"
    
    if func_name not in globals():
        print(json.dumps({{"error": f"Function '{{func_name}}' not found. Please declare 'def {{func_name}}(...)'"}}))
        sys.exit(0)
        
    func = globals()[func_name]
    results = []
    all_passed = True
    
    for i, tc in enumerate(test_cases):
        args = tc.get("input", [])
        expected = tc.get("expected")
        is_sample = tc.get("is_sample", False)
        
        try:
            # Handle args passing (list of args)
            if isinstance(args, list):
                actual = func(*args)
            elif isinstance(args, dict):
                actual = func(**args)
            else:
                actual = func(args)
                
            passed = (actual == expected)
            if not passed:
                all_passed = False
                
            item = {{
                "test_index": i + 1,
                "passed": passed,
                "is_sample": is_sample,
                "actual": actual if is_sample or not passed else None
            }}
            results.append(item)
        except Exception as e:
            all_passed = False
            results.append({{
                "test_index": i + 1,
                "passed": False,
                "is_sample": is_sample,
                "error": str(e)
            }})
            
    print(json.dumps({{"results": results, "all_passed": all_passed}}))

if __name__ == "__main__":
    main()
"""

def execute_coding_exercise(
    user_code: str,
    function_name: str,
    test_cases: List[Dict[str, Any]],
    timeout_seconds: float = 3.0
) -> Dict[str, Any]:
    """
    Executes user Python code against deterministic test cases in an isolated subprocess
    with AST security inspection and strict execution time limits.
    """
    # 1. Static security validation
    security_errors = validate_code_safety(user_code)
    if security_errors:
        return {
            "passed": False,
            "passed_tests": 0,
            "total_tests": len(test_cases),
            "runtime_ms": 0.0,
            "error": "Security Restriction: " + " | ".join(security_errors),
            "results": []
        }

    # 2. Prepare test harness script in temporary file
    harness_code = HARNESS_TEMPLATE.format(
        user_code=user_code,
        test_cases_json=json.dumps(test_cases),
        function_name=function_name
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
        temp_file.write(harness_code)
        temp_path = temp_file.name

    start_time = time.time()
    try:
        # Run in separate Python process with timeout
        proc = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        
        if proc.returncode != 0:
            err = proc.stderr.strip() or proc.stdout.strip() or "Runtime error occurred during test execution."
            return {
                "passed": False,
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "runtime_ms": elapsed_ms,
                "error": err,
                "results": []
            }
            
        try:
            output_data = json.loads(proc.stdout.strip())
        except json.JSONDecodeError:
            return {
                "passed": False,
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "runtime_ms": elapsed_ms,
                "error": f"Failed to parse test output: {proc.stdout.strip()}",
                "results": []
            }

        if "error" in output_data:
            return {
                "passed": False,
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "runtime_ms": elapsed_ms,
                "error": output_data["error"],
                "results": []
            }

        harness_results = output_data.get("results", [])
        passed_count = sum(1 for r in harness_results if r.get("passed"))
        all_passed = (passed_count == len(test_cases))

        # Format user-facing results, safeguarding hidden test data
        sanitized_results = []
        for i, r in enumerate(harness_results):
            tc = test_cases[i] if i < len(test_cases) else {}
            is_sample = tc.get("is_sample", False)
            
            item = {
                "test_index": r["test_index"],
                "passed": r["passed"],
                "error": r.get("error")
            }
            if is_sample:
                item["input_str"] = json.dumps(tc.get("input"))
                item["expected_str"] = json.dumps(tc.get("expected"))
                item["actual_str"] = json.dumps(r.get("actual"))
            else:
                if not r["passed"]:
                    item["actual_str"] = "Output did not match expected value"
                item["input_str"] = "[Hidden test case]"
                item["expected_str"] = "[Hidden test case]"

            sanitized_results.append(item)

        return {
            "passed": all_passed,
            "passed_tests": passed_count,
            "total_tests": len(test_cases),
            "runtime_ms": elapsed_ms,
            "error": None if all_passed else f"Completed {passed_count}/{len(test_cases)} tests successfully.",
            "results": sanitized_results
        }

    except subprocess.TimeoutExpired:
        return {
            "passed": False,
            "passed_tests": 0,
            "total_tests": len(test_cases),
            "runtime_ms": round(timeout_seconds * 1000, 2),
            "error": f"Time Limit Exceeded ({timeout_seconds}s). Ensure code avoids infinite loops or excessive recursion.",
            "results": []
        }
    except Exception as e:
        return {
            "passed": False,
            "passed_tests": 0,
            "total_tests": len(test_cases),
            "runtime_ms": 0.0,
            "error": f"Execution error: {str(e)}",
            "results": []
        }
