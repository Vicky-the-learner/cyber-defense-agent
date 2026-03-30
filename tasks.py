TASKS = {
    "easy": [
        {"input": "' OR 1=1 --", "expected_attack": "SQL Injection"},
        {"input": "<script>alert(1)</script>", "expected_attack": "XSS"}
    ],
    "medium": [
        {"input": "admin' OR '1'='1", "expected_attack": "SQL Injection"},
        {"input": "<img src=x onerror=alert(1)>", "expected_attack": "XSS"}
    ],
    "hard": [
        {"input": "' UNION SELECT password FROM users --", "expected_attack": "SQL Injection"},
        {"input": "<svg/onload=alert(1)>", "expected_attack": "XSS"}
    ]
}