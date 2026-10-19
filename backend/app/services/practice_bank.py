from typing import List, Dict, Any

CODING_PROBLEMS_CATALOG: List[Dict[str, Any]] = [
    {
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "category": "Arrays & HashMaps",
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice. Return the indices sorted in ascending order `[i, j]`.",
        "starter_code": "def two_sum(nums, target):\n    # Write your solution here\n    pass\n",
        "function_name": "two_sum",
        "hints": [
            "A brute force approach checks all pairs in O(N^2) time.",
            "Can you use a hash map to look up the complement (target - num) in O(1) time?"
        ],
        "test_cases": [
            {"input": [[2, 7, 11, 15], 9], "expected": [0, 1], "is_sample": True},
            {"input": [[3, 2, 4], 6], "expected": [1, 2], "is_sample": True},
            {"input": [[3, 3], 6], "expected": [0, 1], "is_sample": False},
            {"input": [[1, 5, 8, 12, 19], 20], "expected": [0, 4], "is_sample": False}
        ],
        "solution_approach": "Use a dictionary `seen = {}`. For each index `i` and number `num`, compute `diff = target - num`. If `diff` is in `seen`, return `[seen[diff], i]`. Otherwise store `seen[num] = i`. Runs in O(N) time and O(N) space."
    },
    {
        "slug": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "Easy",
        "category": "Two Pointers",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nGiven a string `s`, return `True` if it is a palindrome, or `False` otherwise.",
        "starter_code": "def is_palindrome(s: str) -> bool:\n    # Write your solution here\n    pass\n",
        "function_name": "is_palindrome",
        "hints": [
            "Filter the string to keep only alphanumeric characters in lowercase.",
            "Use two pointers: one at the start, one at the end, moving towards the center."
        ],
        "test_cases": [
            {"input": ["A man, a plan, a canal: Panama"], "expected": True, "is_sample": True},
            {"input": ["race a car"], "expected": False, "is_sample": True},
            {"input": [" "], "expected": True, "is_sample": False},
            {"input": ["0P"], "expected": False, "is_sample": False}
        ],
        "solution_approach": "Clean the string with `filtered = [c.lower() for c in s if c.isalnum()]` and return `filtered == filtered[::-1]`, or compare with two pointers in O(N) time."
    },
    {
        "slug": "best-time-to-buy-and-sell-stock",
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "category": "Arrays",
        "description": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "starter_code": "def max_profit(prices):\n    # Write your solution here\n    pass\n",
        "function_name": "max_profit",
        "hints": [
            "Track the minimum buying price seen so far as you iterate through the list.",
            "Calculate profit if sold on the current day: current_price - min_price."
        ],
        "test_cases": [
            {"input": [[7, 1, 5, 3, 6, 4]], "expected": 5, "is_sample": True},
            {"input": [[7, 6, 4, 3, 1]], "expected": 0, "is_sample": True},
            {"input": [[2, 4, 1]], "expected": 2, "is_sample": False},
            {"input": [[3, 2, 6, 5, 0, 3]], "expected": 4, "is_sample": False}
        ],
        "solution_approach": "Maintain `min_price = float('inf')` and `max_profit = 0`. For `p` in prices: `min_price = min(min_price, p)`, `max_profit = max(max_profit, p - min_price)`. O(N) time, O(1) space."
    },
    {
        "slug": "container-with-most-water",
        "title": "Container With Most Water",
        "difficulty": "Medium",
        "category": "Two Pointers",
        "description": "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`.\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.",
        "starter_code": "def max_area(height):\n    # Write your solution here\n    pass\n",
        "function_name": "max_area",
        "hints": [
            "Start with the widest container: left pointer at 0, right pointer at n-1.",
            "The area is limited by the shorter line. Which pointer should move to potentially find a larger area?"
        ],
        "test_cases": [
            {"input": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "expected": 49, "is_sample": True},
            {"input": [[1, 1]], "expected": 1, "is_sample": True},
            {"input": [[4, 3, 2, 1, 4]], "expected": 16, "is_sample": False},
            {"input": [[1, 2, 1]], "expected": 2, "is_sample": False}
        ],
        "solution_approach": "Two pointers `l = 0, r = len(height) - 1`. While `l < r`: `area = min(height[l], height[r]) * (r - l)`. Move the pointer corresponding to the shorter height inward. O(N) time, O(1) space."
    }
]

SQL_PROBLEMS_CATALOG: List[Dict[str, Any]] = [
    {
        "slug": "employees-in-engineering-dept",
        "title": "Engineering Department Employees",
        "difficulty": "Easy",
        "category": "JOINs",
        "prompt": "Write a SQL query to retrieve the `first_name`, `last_name`, and `salary` of all employees working in the 'Engineering' department. Order the results by `salary` descending.",
        "schema_info": "Tables available: `employees(emp_id, first_name, last_name, dept_id, salary, hire_date, role)` and `departments(dept_id, dept_name, location)`",
        "expected_sql": "SELECT e.first_name, e.last_name, e.salary FROM employees e JOIN departments d ON e.dept_id = d.dept_id WHERE d.dept_name = 'Engineering' ORDER BY e.salary DESC;",
        "hints": [
            "Join `employees` and `departments` using `dept_id`.",
            "Filter where `dept_name = 'Engineering'`."
        ],
        "explanation": "An INNER JOIN matches employees with their department. Filtering on `dept_name = 'Engineering'` isolates engineering staff, and `ORDER BY e.salary DESC` ensures highest earners appear first."
    },
    {
        "slug": "average-salary-by-department",
        "title": "Average Department Salary",
        "difficulty": "Medium",
        "category": "GROUP BY & Aggregations",
        "prompt": "Write a SQL query to display each department's `dept_name`, the count of employees as `employee_count`, and their rounded average salary as `avg_salary` (rounded to 2 decimal places). Order by `avg_salary` descending.",
        "schema_info": "Tables available: `employees(emp_id, first_name, last_name, dept_id, salary, hire_date, role)` and `departments(dept_id, dept_name, location)`",
        "expected_sql": "SELECT d.dept_name, COUNT(e.emp_id) AS employee_count, ROUND(AVG(e.salary), 2) AS avg_salary FROM departments d JOIN employees e ON d.dept_id = e.dept_id GROUP BY d.dept_id, d.dept_name ORDER BY avg_salary DESC;",
        "hints": [
            "Use `COUNT(e.emp_id)` and `ROUND(AVG(e.salary), 2)`.",
            "Group by department to compute aggregates per department."
        ],
        "explanation": "Grouping by department enables aggregate calculation over employees in each group. `AVG(salary)` calculates mean pay, while `ROUND(..., 2)` formats the currency value."
    },
    {
        "slug": "top-students-above-9-gpa",
        "title": "Honor Roll Students & Enrollments",
        "difficulty": "Medium",
        "category": "Subqueries & Filtering",
        "prompt": "Write a SQL query to find all students (`student_id`, `name`, `gpa`) who have a GPA greater than or equal to 9.0 and are enrolled in 'Data Structures & Algorithms' (course_id = 'CS101'). Order by `gpa` descending.",
        "schema_info": "Tables available: `students(student_id, name, major, gpa, graduation_year)` and `enrollments(enrollment_id, student_id, course_id, grade, score)`",
        "expected_sql": "SELECT s.student_id, s.name, s.gpa FROM students s JOIN enrollments e ON s.student_id = e.student_id WHERE s.gpa >= 9.0 AND e.course_id = 'CS101' ORDER BY s.gpa DESC;",
        "hints": [
            "Join `students` with `enrollments` on `student_id`.",
            "Add conditions for GPA >= 9.0 and course_id = 'CS101'."
        ],
        "explanation": "Joining students and enrollments filters out students who are not in the specified course while enforcing the honor roll GPA threshold."
    },
    {
        "slug": "orders-revenue-completed",
        "title": "Completed Orders Revenue Summary",
        "difficulty": "Easy",
        "category": "Aggregations",
        "prompt": "Write a SQL query that retrieves the count of completed orders as `order_count` and total revenue as `total_revenue` for orders with `status = 'Completed'`.",
        "schema_info": "Table available: `orders(order_id, customer_name, order_date, total_amount, status)`",
        "expected_sql": "SELECT COUNT(*) AS order_count, SUM(total_amount) AS total_revenue FROM orders WHERE status = 'Completed';",
        "hints": [
            "Filter rows where status = 'Completed'.",
            "Use `COUNT(*)` and `SUM(total_amount)`."
        ],
        "explanation": "Aggregation functions `COUNT` and `SUM` operate over the subset of rows matching the WHERE condition to compute overall volume and gross revenue."
    }
]

def seed_practice_problems(db_session) -> None:
    """Seeds coding and SQL problems into the database."""
    from backend.app.models.practice import CodingProblem, SqlProblem
    
    # 1. Coding Problems
    for cp in CODING_PROBLEMS_CATALOG:
        exists = db_session.query(CodingProblem).filter(CodingProblem.slug == cp["slug"]).first()
        if not exists:
            new_cp = CodingProblem(
                slug=cp["slug"],
                title=cp["title"],
                difficulty=cp["difficulty"],
                category=cp["category"],
                description=cp["description"],
                starter_code=cp["starter_code"],
                function_name=cp["function_name"],
                test_cases=cp["test_cases"],
                hints=cp["hints"],
                solution_approach=cp["solution_approach"]
            )
            db_session.add(new_cp)

    # 2. SQL Problems
    for sp in SQL_PROBLEMS_CATALOG:
        exists = db_session.query(SqlProblem).filter(SqlProblem.slug == sp["slug"]).first()
        if not exists:
            new_sp = SqlProblem(
                slug=sp["slug"],
                title=sp["title"],
                difficulty=sp["difficulty"],
                category=sp["category"],
                prompt=sp["prompt"],
                schema_info=sp["schema_info"],
                expected_sql=sp["expected_sql"],
                hints=sp["hints"],
                explanation=sp["explanation"]
            )
            db_session.add(new_sp)

    db_session.commit()
