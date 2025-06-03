# PlusRequest

**PlusRequest** is a Django REST Framework (DRF) extension that enhances the standard `Request` with first-class support for timestamp-based synchronization and typed metadata access.

It adds a structured way to compare client and server timestamps, detect when updates are needed, and manage API headers in a consistent, testable manner.

---

## Features

- ✅ `PlusRequest`: subclass of DRF’s `Request` with timestamp parsing & comparison
- 🧠 `TimestampOp`: context-aware timestamp diff logic (`client_is_newer`, etc.)
- ⚙️ Configurable via `PlusRequestConf` (env vars or `settings.PLUSREQUEST_CONF`)
- 🧾 Typed request metadata with `Meta`, `PlusMeta`, and `DefaultMeta`
- 🔒 Built-in error handling for missing or invalid timestamps

---

## Installation

```bash
pip install git+https://github.com/huncholane/django-plusrequest
````

Make sure your project has a valid `setup.py` or `pyproject.toml`.

---

## Usage

### Example View

```python
from plusrequest.request import PlusRequest

def view(request: PlusRequest):
    op = request.ts_builder(instance=model)
    if op.client_is_newer:
        return Response("No update needed.")
    # else send new data
    return Response(data)
```

---

## Timestamp Comparison

The `TimestampOp` class is accessed via `request.top_builder(...)`. It automatically:

* Extracts server timestamps from a model instance
* Parses client timestamps from headers or body
* Validates datetime format
* Raises errors or returns status flags

### Supported behaviors

* `raise_get`
* `raise_update`

---

## Configuration

Set via environment variables or in `settings.PLUSREQUEST_CONF`:

| Key                                    | Default               | Description                                                   |
| -------------------------------------- | --------------------- | ------------------------------------------------------------- |
| `PLUSREQUEST_HEADER_TIMESTAMP_FIELD`   | `lastUpdated`         | Header field used for client timestamp                        |
| `PLUSREQUEST_BODY_TIMESTAMP_FIELD`     | `lastUpdated`         | Body field used for client timestamp                          |
| `PLUSREQUEST_INSTANCE_TIMESTAMP_FIELD` | `lastUpdated`         | Model field used for server timestamp                         |
| `PLUSREQUEST_NOUPDATE_CODE`            | `418`                 | Error code raised when update is unnecessary                  |
| `PLUSREQUEST_MISSING_ACTION`           | `noupdate`            | Action if timestamp is missing (`error`, `allow`, `noupdate`) |
| `PLUSREQUEST_DATETIME_FORMAT`          | `%Y-%m-%dT%H:%M:%S%z` | Timestamp parsing format                                      |

---

## Typed Metadata Access

Use `Meta` for strongly-typed access to `request.META`.

```python
from plusrequest.meta import Meta

def view(request: PlusRequest):
    meta: Meta = request.META
    user_agent = meta.get("HTTP_USER_AGENT")
    ip = meta.get("HTTP_X_REAL_IP") or meta.get("REMOTE_ADDR")
```

### Meta Types

* `DefaultMeta`: Core Django fields (e.g. `HTTP_HOST`, `REQUEST_METHOD`)
* `PlusMeta`: Common API headers (e.g. `HTTP_AUTHORIZATION`, `HTTP_X_APP_VERSION`)
* `Meta`: Union of both

---

## Exceptions

* `InvalidClientDatetimeField`
* `InvalidServerDatetimeField`
* `NoUpdate`

Raised when timestamps are missing, malformatted, or update should be skipped.

---

## Project Structure

```
plusrequest/
├── request.py       # PlusRequest class
├── timestamp_op.py  # TimestampOp logic
├── meta.py          # TypedDict for request.META
├── settings.py      # Loads PlusRequestConf
├── types.py         # Custom enums or aliases
```

---

## License

MIT License

```

---

Let me know if you want:
- Examples for writing tests with `PlusRequest`
- Sphinx or `mkdocs` setup
- DRF `APIView` integration patterns
```
