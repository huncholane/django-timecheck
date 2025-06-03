# TimeCheck

**TimeCheck** is a Django REST Framework (DRF) extension that wraps the standard `Request` with first-class support for timestamp-based synchronization.

It adds a structured way to compare client and server timestamps, detect when updates are needed, and manage API headers in a consistent, testable manner.

---

## Features

- 🧠 `TimeCheck`: context-aware timestamp diff logic (`raise_get`, etc.)
- ⚙️ Configurable via `TimeCheckConf` (env vars or `settings.TIMECHECK_CONF`)
- 🔒 Built-in error handling for missing or invalid timestamps

---

## Installation

```bash
pip install git+https://github.com/huncholane/django-timecheck
````

---

## Usage

### Example View

```python
from timecheck import TimeCheck
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MyModel

class MyView(APIView):
    def get(request: Request, pk:int):
        instance = MyModel.objects.get(pk=pk)
        TimeCheck(request,instance).check_time() # throws rest framework exception
        ...
        return Response(data)

    def put(request: Request, pk:int):
        instance = MyModel.objects.get(pk=pk)
        TimeCheck(request,instance).check_update() # throws rest framework exception
        ...
        return Response(data)
```

---

### Parameters

TimeCheck(request, ...) has the following arguments:

- **request** `rest_framework.request.Request`: A request to extract the client timestamp from. (required)
- **instance** `models.Model`: The database instance to extract the server timestamp from using the instance field. (optional)
- **server_timestamp** `dt.datetime`: A manual server timestamp to override TimeCheck parsing.(optional)
- **client_timestamp** `dt.datetime`: A manual client timestamp to override TimeCheck parsing. (optional)
- **header_field** `str`: Field to find client timestamp in the header (defaults to config)
- **body_field** `str`: Field to find client timestamp in request body (defaults to config)
- **instance_field** `str`: Field to find server timestamp in database model (defaults to config)
- **missing_action**: `"noupdate" | "continue"` (defaults to config)
  - `noupdate` will raise a drf exception to indicate the view should stop early if the client does not provide a timestamp
  - `continue` allows the view to continue processing data when the client does not provide a timestamp
- **noupdate_code** `int` The response code for exceptions raised to indicate the view should stop processing
- **dt_fmt** `str` The datetime format used to normalize timestamps. Useful when the client and server use mismatched time depths (defaults to config)
- **raise_exception** `bool` Raises and exception if the process should stop (defaults to config)

### TimeCheck Methods

- `should_get` Raises a `NoUpdate` exception when the client timestamp is newer than or equal to the server timestamp. Returns a True if the client should receive data.
- `check_update` Raises a `NoUpdate` exception when the client timestamp is older than or equal to the server timestamp. Returns a True if the update should continue.

---

## Configuration

TimeCheck is customizable through the django settings, env, and on a per usage basis.

### Django Settings Dictionairy (Defaults)

```python
TIMECHECK_CONF = {
    "body_field": "lastUpdated",
    "dt_fmt": "%Y-%m-%dT%H:%M:%S%z",
    "header_field": "lastUpdated",
    "instance_field": "lastUpdated",
    "missing_action": "noupdate",
    "noupdate_code": 418,
    "raise_exception": True,
}
```

###

Set via environment variables or in `settings.TIMECHECK_CONF`:

| Key                                    | Default               | Description                                                   |
| -------------------------------------- | --------------------- | ------------------------------------------------------------- |
| `TIMECHECK_HEADER_FIELD`   | `lastUpdated`         | Header field used for client timestamp (str)                        |
| `TIMECHECK_BODY_FIELD`     | `lastUpdated`         | Body field used for client timestamp (str)                         |
| `TIMECHECK_INSTANCE_FIELD` | `lastUpdated`         | Model field used for server timestamp (str)                         |
| `TIMECHECK_NOUPDATE_CODE`            | `418`                 | Error code raised when update is unnecessary (int)                 |
| `TIMECHECK_MISSING_ACTION`           | `noupdate`            | Action if timestamp is missing (`continue`, `noupdate`) |
| `TIMECHECK_DT_FMT`          | `%Y-%m-%dT%H:%M:%S%z` | Timestamp parsing format (str)                                     |
| RAISE_EXCEPTION | True | Raises exceptions by default (bool) |

---

## Exceptions

- `InvalidClientDatetimeField (400)` When the client timestamp is found but cannot be parsed.
- `InvalidServerDatetimeField (500)` When the server cannot make up a timestamp.
- `NoUpdate (Custom)` Custom status code used to represent no update.

Raised when timestamps are missing, malformatted, or update should be skipped.

---

## License

This project is licensed under the [MIT License](LICENSE).
