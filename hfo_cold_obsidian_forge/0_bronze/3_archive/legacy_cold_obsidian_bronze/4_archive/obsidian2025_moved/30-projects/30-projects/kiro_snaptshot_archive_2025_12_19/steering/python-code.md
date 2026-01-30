---
hfo:
  gen: 78
  ts: 2025-12-19T19:08:48.203Z
  port: 7
  role: NAVIGATE
  trigram: ☰
  pillar: Navigator
  greek: Κυβέρνησις
  phase: REACT
  status: active
  desc: python-code
---

---
inclusion: fileMatch
fileMatchPattern: "**/*.py"
---

# Python Code Standards (HFO Gen 76)

## Type Hints
- All functions MUST have type hints for parameters and return values
- Use `list[T]` not `List[T]` (Python 3.9+)
- Use `dict[K, V]` not `Dict[K, V]`
- Use `X | None` not `Optional[X]`

## Formatting
- Use `ruff` for formatting and linting
- Line length: 120 characters max
- Imports: stdlib → third-party → local (separated by blank lines)

## Docstrings
- All public functions MUST have docstrings
- Use Google-style docstrings:
  ```python
  def func(arg: str) -> int:
      """Short description.

      Args:
          arg: Description of arg

      Returns:
          Description of return value
      """
  ```

## Error Handling
- Return structured errors with `error_code` field
- Log errors to blackboard pathos field via `log_error()`
- Never silently swallow exceptions

## Async
- Prefer `async/await` for I/O operations
- Use `httpx.AsyncClient` for HTTP requests
- Name async functions with `_async` suffix when sync wrapper exists
