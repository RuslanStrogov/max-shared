# max-shared

Shared core library for MAX Bot API clients.

## Purpose

This package eliminates code duplication between:

- **max-hermes** — standalone bridge daemon (aiohttp + Hermes CLI)
- **max-hermes-plugin** — Hermes Agent platform plugin

## Modules

| Module | Purpose |
|--------|---------|
| `constants` | Shared constants (API URLs, timeouts, limits, update types) |
| `models` | Pydantic models for MAX Bot API (updates, messages, attachments) |
| `max_client` | Async HTTP client for MAX Bot API |
| `converter` | Format converter between MAX API and internal message format |
| `markdown` | Shared markdown detection and stripping utilities |

## Installation

```bash
pip install -e /path/to/max-shared
```

Or in requirements.txt:

```
max-shared @ file:///path/to/max-shared
```

## Usage

```python
from max_shared.max_client import MAXClient
from max_shared.converter import MessageConverter
from max_shared.markdown import has_markdown

# API client
client = MAXClient(token="your-bot-token")
bot_info = await client.get_bot_info()

# Converter
payload = MessageConverter.max_update_to_message(update)
max_msg = MessageConverter.response_to_max_message(response, user_id=123)

# Markdown
if has_markdown(text):
    payload["format"] = "markdown"
```

## License

MIT
