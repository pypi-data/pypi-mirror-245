# Vaultinum Timestamping Python SDK

This module is a simple client for the Vaultinum's Timestamping service.

## Installation

This package is available on PyPI :

```bash
python -m pip install vaultinum-ts
```

## Usage

```python
>>> from vaultinum_ts import timestamp
>>> timestamp("data.txt", "sandbox", "YOUR_SANDBOX_APIKEY")
```
