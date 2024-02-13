# Overview

Simple app to run an API that lets you find open restaurants at a given date and
time.

# Setup

```
pip install -r requirements.txt
```

# Run Endpoint

```
python run_app.py
```

This runs a local server that accepts GET requests to the `restaurants` endpoint.
Only one argument is passed, `datetime`, which must be an isoformatted time:
`%Y-%m-%dT%H:%M`. The returned value is a list of all restaurants open
at the given input.

For example, the payload
```
{
    "datetime": "2024-02-10T00:00"
}
```

yields the response
```
{
    "data": [
        "Bonchon",
        "Seoul 116",
        "The Cheesecake Factory"
    ]
}
```

# Testing

From the project directory run
```
python -m pytest
```