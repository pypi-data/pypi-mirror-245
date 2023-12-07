# Project description

**JSONEyeX** is a Python package that provides an easy-to-use and robust solution for validating JSON data against a predefined schema. Designed to handle various data types and structures, including nested JSON objects, **JSONEyeX** ensures your data adheres to the specified format and types, enhancing the reliability of your applications that process JSON data.

## Features:

- Validates standard JSON data types, including strings, numbers, objects, and lists.
- Supports custom validation for nested JSON structures.
- Provides clear, descriptive error messages for quick debugging.
- Easy integration into existing Python projects.

## Ideal for:

- Data validation in web APIs.
- Ensuring data integrity in data processing pipelines.
- Rapid development in scenarios where JSON data structures are extensively used.

**JSONEyeX** is simple yet powerful, making it an essential tool for any project that requires JSON data validation.

## Example Usage:

Here is a simple example demonstrating how to use **JSONEyeX** to validate a JSON object:

## Datatype Map

This datatype can be used
```
    {
        "string": str,
        "number": (int, float),
        "object": dict,
        "list": list
    }
```

```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"}
            },
            "required": ["street", "city"]
        }
    },
    "required": ["name", "age", "address"]
}

data = {
    "name": "John Doe",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "Anytown"
    }
}

from JSONEyeX import jsonvalidator

try:
    validator = jsonvalidator(schema, data)
    print("No errors, validation successful.")
except ValueError as e:
    print(f"Validation error: {e}")
```