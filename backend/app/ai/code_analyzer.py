import ast
import json
import logging
from typing import Dict, Any, List
from backend.app.ai.gemini_provider import GeminiProvider

logger = logging.getLogger("careerforge.code_analyzer")

def _ast_fallback_analysis(problem_title: str, code: str) -> Dict[str, Any]:
    """Deterministic AST-based complexity analyzer for offline or fallback execution."""
    try:
        tree = ast.parse(code)
    except Exception as e:
        return {
            "time_complexity": "Syntax Error",
            "space_complexity": "N/A",
            "summary": f"Could not parse code: {str(e)}",
            "bottlenecks": "Code contains syntax errors preventing static analysis.",
            "optimization_advice": "Ensure Python code has valid indentation and syntax before analyzing.",
            "edge_cases": ["Syntax validation"],
            "model_used": "Deterministic Static Analyzer"
        }

    # Count for-loops, while-loops, and nested loops
    loop_depth = 0
    max_loop_depth = 0
    has_hash_map = False
    has_recursion = False

    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_depth = 0
            self.max_depth = 0
            self.uses_dict = False
            self.uses_set = False
            self.func_names = set()

        def visit_FunctionDef(self, node):
            self.func_names.add(node.name)
            self.generic_visit(node)

        def visit_For(self, node):
            self.current_depth += 1
            if self.current_depth > self.max_depth:
                self.max_depth = self.current_depth
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_While(self, node):
            self.current_depth += 1
            if self.current_depth > self.max_depth:
                self.max_depth = self.current_depth
            self.generic_visit(node)
            self.current_depth -= 1

        def visit_Dict(self, node):
            self.uses_dict = True
            self.generic_visit(node)

        def visit_Set(self, node):
            self.uses_set = True
            self.generic_visit(node)

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    depth = visitor.max_depth
    if depth == 0:
        time_comp = "O(1) - Constant Time"
        time_desc = "Executes with a fixed number of operations independent of input size."
    elif depth == 1:
        time_comp = "O(N) - Linear Time"
        time_desc = "Single pass through the input collections."
    elif depth == 2:
        time_comp = "O(N²) - Quadratic Time"
        time_desc = "Nested iteration detected. This may cause Time Limit Exceeded (TLE) on large inputs (N > 10^4)."
    else:
        time_comp = f"O(N^{depth}) - Polynomial Time"
        time_desc = "Multiple nested loops detected. High risk of timeout."

    if visitor.uses_dict or visitor.uses_set:
        space_comp = "O(N) - Linear Auxiliary Space"
        space_desc = "Allocates extra memory proportional to the input using a hash table / set."
    else:
        space_comp = "O(1) - Constant Space"
        space_desc = "Modifies state in-place with minimal pointer variables."

    bottlenecks = (
        "Nested loop traversal will degrade performance significantly when input size exceeds 5,000 elements."
        if depth >= 2 else
        "Single pass iteration is optimal for array traversal. No major nested bottlenecks detected."
    )

    optimization_advice = (
        "Consider replacing inner nested loops with a hash map lookup (reducing O(N²) to O(N)) or sorting with two pointers."
        if depth >= 2 else
        "Ensure memory usage remains O(1) where possible by avoiding unnecessary intermediate array copies."
    )

    edge_cases = [
        "Empty collection / None input",
        "Single element list",
        "Duplicate elements",
        "Negative numbers & zero values",
        "Large scale inputs (10^5 elements)"
    ]

    return {
        "time_complexity": time_comp,
        "space_complexity": space_comp,
        "summary": f"{time_desc} {space_desc}",
        "bottlenecks": bottlenecks,
        "optimization_advice": optimization_advice,
        "edge_cases": edge_cases,
        "model_used": "Deterministic AST Static Analyzer"
    }

def analyze_code_complexity(problem_title: str, code: str) -> Dict[str, Any]:
    """Analyzes code complexity using Gemini LLM if available, with robust AST fallback."""
    provider = GeminiProvider()
    if provider.is_configured():
        prompt = f"""You are a Lead Software Development Engineer interviewer at a Tier-1 tech company.
Analyze this Python code submitted for '{problem_title}':

```python
{code}
```

Return your analysis strictly in valid JSON format with these exact keys:
{{
  "time_complexity": "e.g. O(N) or O(N log N)",
  "space_complexity": "e.g. O(1) or O(N)",
  "summary": "Concise 1-2 sentence engineering summary of the approach",
  "bottlenecks": "Identify specific line numbers or structures causing highest computational cost",
  "optimization_advice": "Actionable technical advice for Tier-1 interview clearance",
  "edge_cases": ["Edge case 1", "Edge case 2", "Edge case 3"]
}}
Do not wrap in markdown quotes if possible, output pure JSON."""
        try:
            raw_response = provider.generate_text(
                prompt=prompt,
                system_instruction="You are a strict Big-O algorithm analyst for technical interviews. Always respond in pure JSON."
            )
            # Parse JSON
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
            data["model_used"] = "Google Gemini Live Intelligence"
            return data
        except Exception as e:
            logger.warning(f"Gemini code analysis failed: {e}. Falling back to AST analyzer.")

    # Fallback to AST analyzer
    return _ast_fallback_analysis(problem_title, code)

