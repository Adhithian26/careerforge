from typing import List, Dict, Any

QUESTIONS_CATALOG: List[Dict[str, Any]] = [
    # --- PYTHON QUESTIONS ---
    {
        "topic": "Python",
        "subtopic": "Memory & Mutability",
        "difficulty": "Medium",
        "question_text": "What is the output of the following Python snippet?",
        "code_snippet": "def append_to(element, target=[]):\n    target.append(element)\n    return target\n\nlist1 = append_to(10)\nlist2 = append_to(20, [])\nlist3 = append_to(30)\nprint(list1, list3)",
        "options": [
            "[10] [30]",
            "[10, 30] [10, 30]",
            "[10] [10, 30]",
            "[10, 20, 30] [10, 20, 30]"
        ],
        "correct_option_index": 1,
        "explanation": "Default arguments in Python are evaluated once when the function is defined, not each time it is called. Because the default list is mutable, both `append_to(10)` and `append_to(30)` mutate and share the exact same default list object in memory."
    },
    {
        "topic": "Python",
        "subtopic": "Generators",
        "difficulty": "Medium",
        "question_text": "What does the `yield` statement do in a Python function?",
        "code_snippet": None,
        "options": [
            "Terminates the function execution and returns a tuple",
            "Pauses the function, saves execution state, and yields a value to the caller as part of a generator iterator",
            "Spawns an asynchronous coroutine in the background event loop",
            "Allocates contiguous memory for an immutable sequence"
        ],
        "correct_option_index": 1,
        "explanation": "The `yield` keyword turns a regular function into a generator factory. When called, it suspends execution, yields the specified value, and preserves local variables and instruction pointers so execution can resume on `next()`."
    },
    {
        "topic": "Python",
        "subtopic": "GIL & Concurrency",
        "difficulty": "Hard",
        "question_text": "How does the Global Interpreter Lock (GIL) in CPython affect multi-threaded programs?",
        "code_snippet": None,
        "options": [
            "It prevents multiple threads from performing I/O operations simultaneously",
            "It ensures that only one native thread executes Python bytecode at any given moment",
            "It automatically converts multi-threaded programs into distributed processes",
            "It eliminates race conditions between threads accessing shared mutable state"
        ],
        "correct_option_index": 1,
        "explanation": "CPython's GIL is a mutex that protects access to Python objects, preventing multiple native OS threads from executing Python bytecode simultaneously. Multi-threading benefits I/O-bound tasks where the lock is released during I/O, but CPU-bound tasks require multiprocessing to utilize multiple CPU cores."
    },

    # --- SQL QUESTIONS ---
    {
        "topic": "SQL",
        "subtopic": "JOINs",
        "difficulty": "Easy",
        "question_text": "What is the primary difference between a LEFT JOIN and an INNER JOIN?",
        "code_snippet": None,
        "options": [
            "INNER JOIN returns all rows from the right table, while LEFT JOIN returns unmatched rows only",
            "LEFT JOIN returns all rows from the left table even if there is no match in the right table (with NULLs), whereas INNER JOIN returns only rows with matches in both tables",
            "LEFT JOIN can only be used on indexed primary keys",
            "INNER JOIN performs a Cartesian product, whereas LEFT JOIN enforces a theta join"
        ],
        "correct_option_index": 1,
        "explanation": "INNER JOIN restricts output to rows where the join predicate evaluates to TRUE in both tables. LEFT JOIN (or LEFT OUTER JOIN) preserves all rows from the left table, filling in NULL for all right table columns when no match exists."
    },
    {
        "topic": "SQL",
        "subtopic": "Window Functions",
        "difficulty": "Medium",
        "question_text": "What distinguishes `DENSE_RANK()` from `RANK()` in SQL when duplicate values occur?",
        "code_snippet": "SELECT employee_id, salary,\n       RANK() OVER (ORDER BY salary DESC) as rnk,\n       DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rnk\nFROM employees;",
        "options": [
            "RANK() does not skip rank values after duplicates, while DENSE_RANK() skips ranks",
            "DENSE_RANK() assigns consecutive integers without leaving gaps after ties, whereas RANK() leaves gaps corresponding to the number of duplicates",
            "DENSE_RANK() only works with numeric columns, while RANK() works with strings",
            "There is no difference; they are aliases in ANSI SQL"
        ],
        "correct_option_index": 1,
        "explanation": "If two employees tie for 1st place with salary 100k: `RANK()` assigns 1, 1, and the next employee receives 3. `DENSE_RANK()` assigns 1, 1, and the next employee receives 2 (consecutive rank values without gaps)."
    },
    {
        "topic": "SQL",
        "subtopic": "GROUP BY & Aggregates",
        "difficulty": "Medium",
        "question_text": "When must you use the `HAVING` clause instead of the `WHERE` clause?",
        "code_snippet": None,
        "options": [
            "Whenever sorting records by descending timestamp",
            "To filter rows before any groupings are constructed",
            "To filter groups based on aggregate function results (e.g., COUNT(*), AVG(salary))",
            "To join two tables across different database schemas"
        ],
        "correct_option_index": 2,
        "explanation": "The `WHERE` clause filters individual rows before aggregation occurs and cannot reference aggregate functions. The `HAVING` clause filters the aggregated groups after `GROUP BY` has evaluated aggregate functions."
    },

    # --- DSA QUESTIONS ---
    {
        "topic": "DSA",
        "subtopic": "Arrays & Two Pointers",
        "difficulty": "Easy",
        "question_text": "In a sorted array of N numbers, what is the optimal time complexity to find two numbers that sum to target T using the Two-Pointer approach?",
        "code_snippet": None,
        "options": [
            "O(N^2) time and O(N) space",
            "O(N log N) time and O(1) space",
            "O(N) time and O(1) space",
            "O(log N) time and O(N) space"
        ],
        "correct_option_index": 2,
        "explanation": "Because the array is already sorted, placing one pointer at index 0 and one at index N-1 allows shrinking the search window in each step based on whether the current sum is less than or greater than T. This traverses each element at most once: O(N) time and O(1) auxiliary space."
    },
    {
        "topic": "DSA",
        "subtopic": "Linked Lists",
        "difficulty": "Medium",
        "question_text": "Floyd's Cycle-Finding Algorithm (Tortoise and Hare) detects a cycle in a linked list using two pointers moving at speeds 1 and 2. What is its space complexity?",
        "code_snippet": None,
        "options": [
            "O(N) space",
            "O(1) space",
            "O(log N) space",
            "O(N^2) space"
        ],
        "correct_option_index": 1,
        "explanation": "Floyd's algorithm only maintains two reference pointers (slow and fast), requiring O(1) auxiliary memory, unlike hash table approaches that store node addresses in O(N) memory."
    },
    {
        "topic": "DSA",
        "subtopic": "Hash Maps & Complexity",
        "difficulty": "Medium",
        "question_text": "What is the worst-case time complexity of a hash table lookup when all keys hash to the same bucket in an unmitigated separate chaining implementation?",
        "code_snippet": None,
        "options": [
            "O(1)",
            "O(log N)",
            "O(N)",
            "O(N log N)"
        ],
        "correct_option_index": 2,
        "explanation": "In the worst case (e.g. hash collision attack or degenerate hash function), all N keys collide in the same bucket, turning the bucket into a linear linked list of length N, resulting in O(N) search time."
    },

    # --- OOP QUESTIONS ---
    {
        "topic": "OOP",
        "subtopic": "Core Principles",
        "difficulty": "Easy",
        "question_text": "Which Object-Oriented principle is demonstrated by restricting direct external access to internal object state and requiring interaction through public methods?",
        "code_snippet": None,
        "options": [
            "Polymorphism",
            "Encapsulation",
            "Inheritance",
            "Abstraction"
        ],
        "correct_option_index": 1,
        "explanation": "Encapsulation bundles data and methods that operate on that data into a single unit (class) while restricting direct access to components (data hiding), maintaining internal integrity."
    },
    {
        "topic": "OOP",
        "subtopic": "SOLID Principles",
        "difficulty": "Medium",
        "question_text": "According to the Liskov Substitution Principle (LSP), which of the following statements must hold true?",
        "code_snippet": None,
        "options": [
            "A class should only have one reason to change",
            "Subtypes must be substitutable for their base types without altering the correctness of the program",
            "High-level modules should not depend on low-level modules; both should depend on abstractions",
            "Interfaces should contain as many methods as possible to avoid code duplication"
        ],
        "correct_option_index": 1,
        "explanation": "LSP states that objects of a superclass should be replaceable with objects of a subclass without affecting the correctness or expected behavior of the program."
    },

    # --- DBMS QUESTIONS ---
    {
        "topic": "DBMS",
        "subtopic": "Transactions & ACID",
        "difficulty": "Medium",
        "question_text": "What does the 'I' (Isolation) in ACID transaction properties guarantee?",
        "code_snippet": None,
        "options": [
            "Transactions survive system crashes once committed",
            "Either all operations in the transaction succeed, or all are rolled back",
            "Concurrent transactions execute without interfering with one another, producing results identical to serial execution",
            "Database constraints are never violated before or after a transaction"
        ],
        "correct_option_index": 2,
        "explanation": "Isolation guarantees that concurrently executing transactions cannot view intermediate, uncommitted states of other transactions, preventing anomalies like dirty reads, non-repeatable reads, and phantom reads."
    },
    {
        "topic": "DBMS",
        "subtopic": "Indexing",
        "difficulty": "Medium",
        "question_text": "Why do relational database engines (e.g., PostgreSQL, MySQL) predominantly use B+ Trees rather than standard Binary Search Trees for disk-based indexing?",
        "code_snippet": None,
        "options": [
            "B+ Trees have a high branching factor, which dramatically reduces tree height and minimizes disk I/O operations",
            "Binary search trees cannot store string keys",
            "B+ Trees require zero memory buffers",
            "Binary search trees do not support in-order traversal"
        ],
        "correct_option_index": 0,
        "explanation": "Disk access is several orders of magnitude slower than RAM. B+ Trees have a very high fan-out (hundreds of keys per node), keeping tree depth small (typically 3-4 levels) and packing disk pages efficiently. Leaf nodes are also linked sequentially for high-performance range scans."
    },

    # --- OPERATING SYSTEMS ---
    {
        "topic": "Operating Systems",
        "subtopic": "Process & Deadlocks",
        "difficulty": "Medium",
        "question_text": "Which of the following is NOT one of the four necessary Coffman conditions required for a deadlock to occur?",
        "code_snippet": None,
        "options": [
            "Mutual Exclusion",
            "Hold and Wait",
            "Preemption Permitted",
            "Circular Wait"
        ],
        "correct_option_index": 2,
        "explanation": "The condition is 'No Preemption' (resources cannot be forcibly confiscated from a process holding them; they must be released voluntarily). If preemption is permitted, deadlocks can be resolved or prevented."
    },
    {
        "topic": "Operating Systems",
        "subtopic": "Virtual Memory",
        "difficulty": "Medium",
        "question_text": "What phenomenon occurs when a system spends more time swapping pages into and out of memory than executing actual instructions?",
        "code_snippet": None,
        "options": [
            "Fragmentation",
            "Thrashing",
            "Starvation",
            "Belady's Anomaly"
        ],
        "correct_option_index": 1,
        "explanation": "Thrashing occurs when the active working sets of running processes exceed available physical RAM. The OS continuously incurs page faults, driving CPU utilization to near zero while disk I/O saturates."
    },

    # --- COMPUTER NETWORKS ---
    {
        "topic": "Computer Networks",
        "subtopic": "Transport Layer",
        "difficulty": "Easy",
        "question_text": "What sequence of packets establishes a reliable connection in the standard TCP 3-way handshake?",
        "code_snippet": None,
        "options": [
            "SYN -> ACK -> FIN",
            "SYN -> SYN-ACK -> ACK",
            "ACK -> SYN -> DATA",
            "HELLO -> VERIFY -> CONNECT"
        ],
        "correct_option_index": 1,
        "explanation": "Client sends SYN (with initial sequence number X) -> Server replies with SYN-ACK (acknowledging X+1 and sending initial sequence number Y) -> Client responds with ACK (acknowledging Y+1), establishing full-duplex communication."
    },
    {
        "topic": "Computer Networks",
        "subtopic": "Application Layer & HTTP",
        "difficulty": "Medium",
        "question_text": "What is the primary advantage of HTTP/2 over HTTP/1.1?",
        "code_snippet": None,
        "options": [
            "HTTP/2 eliminates the need for TCP handshakes completely",
            "HTTP/2 introduces binary framing and multiplexing of multiple concurrent requests over a single TCP connection",
            "HTTP/2 is strictly plaintext, making it faster to inspect",
            "HTTP/2 removes status codes like 404 and 500"
        ],
        "correct_option_index": 1,
        "explanation": "HTTP/2 uses binary framing and multiplexing, allowing multiple bidirectional streams of requests and responses to travel concurrently over a single TCP connection, eliminating head-of-line blocking at the application layer."
    },

    # --- APTITUDE QUESTIONS ---
    {
        "topic": "Aptitude",
        "subtopic": "Time & Work",
        "difficulty": "Medium",
        "question_text": "Worker A can complete a software module in 12 days, and Worker B can complete the same module in 24 days. If they work together, how many days will it take them to finish the module?",
        "code_snippet": None,
        "options": [
            "6 days",
            "8 days",
            "9 days",
            "18 days"
        ],
        "correct_option_index": 1,
        "explanation": "Worker A's rate = 1/12 per day. Worker B's rate = 1/24 per day. Combined rate = 1/12 + 1/24 = 2/24 + 1/24 = 3/24 = 1/8 per day. Therefore, together they finish in 8 days."
    },
    {
        "topic": "Aptitude",
        "subtopic": "Probability",
        "difficulty": "Medium",
        "question_text": "Two fair 6-sided dice are rolled simultaneously. What is the probability that the sum of the numbers shown is equal to 8?",
        "code_snippet": None,
        "options": [
            "5/36",
            "1/6",
            "7/36",
            "1/12"
        ],
        "correct_option_index": 0,
        "explanation": "Total possible outcomes = 6 * 6 = 36. Favorable outcomes where sum = 8 are (2,6), (3,5), (4,4), (5,3), (6,2) = 5 outcomes. Probability = 5/36."
    }
]

def seed_assessment_questions(db_session) -> int:
    """Seeds default questions into database if not already present."""
    from backend.app.models.assessment import AssessmentQuestion
    existing_count = db_session.query(AssessmentQuestion).count()
    if existing_count >= len(QUESTIONS_CATALOG):
        return existing_count

    inserted = 0
    for q in QUESTIONS_CATALOG:
        # Check if question text exists
        exists = db_session.query(AssessmentQuestion).filter(
            AssessmentQuestion.question_text == q["question_text"]
        ).first()
        if not exists:
            new_q = AssessmentQuestion(
                topic=q["topic"],
                subtopic=q.get("subtopic"),
                difficulty=q.get("difficulty", "Medium"),
                question_text=q["question_text"],
                code_snippet=q.get("code_snippet"),
                options=q["options"],
                correct_option_index=q["correct_option_index"],
                explanation=q["explanation"]
            )
            db_session.add(new_q)
            inserted += 1

    db_session.commit()
    return inserted
