# Django Scalar Tests

This directory contains test configurations for the Django Scalar package.

## Running Tests

To run the tests, you need to install the test dependencies first:

```bash
uv sync --extra "test"
```

Then you can run the tests with pytest:

```bash
uv run pytest
```

To run the tests with coverage:

```bash
uv run pytest --cov=django_scalar
```

To generate a coverage report:

```bash
uv pytest --cov=django_scalar --cov-report=html
```

## Test Structure

The tests are organized as follows:

- `test_views.py`: Tests for the views module, including:
  - Basic tests for view functionality (status code, template usage).
  - Context data tests that ensure the correct data is passed to the template.
  - End-to-end tests that verify that the HTML content includes expected context data.
  - End-to-end tests that verify the overall structure and integrity of the HTML document.
- `test_get_filter_parameters.py`: Tests for the get_filter_parameters module.
- `test_urls.py`: Tests for the URLs configuration.

## Adding New Tests

When adding new tests, please follow these guidelines:

1. Create a new test file in the `src/django_scalar/tests` directory
2. Use the naming convention `test_*.py` for test files
3. Use the naming convention `Test*` for test classes
4. Use the naming convention `test_*` for test methods
5. Add docstrings to all test classes and methods
6. Use `pytest` and `pytest-django` fixtures where necessary
