# max-shared

> ⚠️ **DEPRECATED** — This library is no longer maintained.
>
> The shared code (models, client, converter) has been merged directly into:
> - [max-hermes](https://github.com/RuslanStrogov/max-hermes) — standalone bridge daemon
> - [max-hermes-plugin](https://github.com/RuslanStrogov/max-hermes-plugin) — Hermes Agent platform plugin
>
> This repository is kept for reference only. Use the individual projects above.

## Purpose (historical)

This package eliminated code duplication between max-hermes and max-hermes-plugin.

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

## Related Projects

| Project | Description |
|---------|-------------|
| [max-hermes](https://github.com/RuslanStrogov/max-hermes) | Standalone bridge daemon — webhook, Docker, systemd |
| [max-hermes-plugin](https://github.com/RuslanStrogov/max-hermes-plugin) | Native Hermes Agent platform plugin |
