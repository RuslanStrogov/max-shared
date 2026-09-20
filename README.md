<div align="center">

  <h1>max-shared</h1>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white" alt="Python"/>
    <img src="https://img.shields.io/badge/MAX-Bot%20API-6366F1?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iIzYzNjZmMSI+PHBhdGggZD0iTTEyIDJMMTggOEwxOCAyMkw2IDIyTDYgOEwxMiAyWiIvPjwvc3ZnPg==&logoColor=white" alt="MAX"/>
    <img src="https://img.shields.io/badge/Pydantic-2.0+-E92063?logo=pydantic&logoColor=white" alt="Pydantic"/>
    <img src="https://img.shields.io/badge/License-MIT-22C55E" alt="MIT"/>
  </p>

  <h3>Общая библиотека для проектов MAX Hermes</h3>
  <p>Shared-модули: MAXClient, Pydantic-модели, конвертер сообщений, утилиты markdown</p>

  <table>
    <tr>
      <td width="50%" align="center">
        <h4>🇷🇺 Российская разработка</h4>
        <p>Open source · MIT</p>
      </td>
      <td width="50%" align="center">
        <h4>⚡ Единый код для bridge и plugin</h4>
        <p>Устраняет дублирование между проектами</p>
      </td>
    </tr>
  </table>

</div>

---

## 📋 Содержание

- [О проекте](#-о-проекте)
- [Модули](#-модули)
- [Установка](#-установка)
- [Использование](#-использование)
- [API клиент (MAXClient)](#-api-клиент-maxclient)
- [Pydantic-модели](#-pydantic-модели)
- [Конвертер сообщений](#-конвертер-сообщений)
- [История изменений](#-история-изменений)
- [Лицензия](#-лицензия)

---

## 📘 О проекте

**max-shared** — общая библиотека, используемая в двух продуктах:

| Проект | Описание | Тип |
|--------|----------|-----|
| [max-hermes](https://github.com/RuslanStrogov/max-hermes) | Самодостаточный мост-демон (aiohttp + Hermes CLI) | standalone |
| [max-hermes-plugin](https://github.com/RuslanStrogov/max-hermes-plugin) | Нативный платформенный плагин для Hermes Gateway | plugin |

Библиотека устраняет дублирование кода — модели запросов/ответов MAX Bot API, HTTP-клиент и конвертер живут в одном месте.

## 📦 Модули

| Модуль | Назначение |
|--------|-----------|
| **`constants`** | Константы: URL API, таймауты, лимиты, типы обновлений |
| **`models`** | Pydantic-модели для MAX Bot API (update, message, attachment) |
| **`max_client`** | Асинхронный HTTP-клиент для MAX Bot API |
| **`converter`** | Конвертер между форматами MAX API и внутренним представлением |
| **`markdown`** | Детектирование и очистка markdown-форматирования |

## 🔧 Установка

```bash
pip install -e /path/to/max-shared
```

Или в `requirements.txt`:

```
max-shared @ file:///path/to/max-shared
```

## 🚀 Использование

```python
from max_shared.max_client import MAXClient
from max_shared.converter import MessageConverter
from max_shared.markdown import has_markdown

# API клиент
client = MAXClient(token="your-bot-token")
bot_info = await client.get_bot_info()

# Конвертер
payload = MessageConverter.max_update_to_message(update)
max_msg = MessageConverter.response_to_max_message(response, user_id=123)

# Markdown
if has_markdown(text):
    payload["format"] = "markdown"
```

## 🎛️ API клиент (MAXClient)

### Основные методы

| Метод | Описание |
|-------|----------|
| `get_bot_info()` | Получить информацию о боте |
| `send_message(chat_id, text, ...)` | Отправить сообщение |
| `edit_message(message_id, chat_id, text, ...)` | Редактировать сообщение |
| `delete_message(message_id, chat_id)` | Удалить сообщение |
| `send_action(chat_id, action)` | Индикатор «Печатает...» |
| `set_commands(commands)` | **Зарегистрировать команды бота (NEW)** |
| `upload_file(file_path, file_name)` | Загрузить файл для отправки |
| `send_file(chat_id, file_id, ...)` | Отправить файл |
| `create_subscription(url, secret)` | Зарегистрировать webhook |
| `get_subscriptions()` | Получить список webhook |
| `delete_subscription(id)` | Удалить webhook |
| `get_updates(params)` | Получить новые события (long polling) |

### `set_commands()`

```python
# Зарегистрировать команды для меню бота
await client.set_commands([
    {"name": "start", "description": "Начать диалог с ботом"},
    {"name": "help", "description": "Помощь и информация о боте"},
    {"name": "about", "description": "О боте и его возможностях"},
])

# Удалить все команды
await client.set_commands([])
```

Команды отправляются на `PATCH /me/commands` через `COMMANDS_API_BASE_URL` (`https://platform-api2.max.ru`).

## 📐 Pydantic-модели

| Модель | Описание |
|--------|---------|
| `Update` | Входящее событие от MAX API |
| `Message` | Сообщение (текст, attachments, кнопки) |
| `Attachment` | Вложение (изображение, видео, аудио, файл) |
| `Button` | Кнопка в inline keyboard |
| `Callback` | Callback от нажатой кнопки |
| `Recipient` | Получатель сообщения |
| `Sender` | Отправитель сообщения |

## 🔄 Конвертер сообщений

| Метод | Описание |
|-------|----------|
| `max_update_to_message(update)` | MAX webhook → внутренний словарь |
| `response_to_max_message(response, ...)` | Ответ Hermes → MAX формат |

## 📄 История изменений

| # | Изменение | Файл |
|---|-----------|------|
| 1 | **`set_commands()`** — новый метод для регистрации команд бота через `PATCH /me/commands` | `max_client.py` |
| 2 | **`COMMANDS_API_BASE_URL`** — новая константа `https://platform-api2.max.ru` для commands API | `constants.py` |
| 3 | **`attachments` → `Optional`** — Pydantic v2 больше не падает на `null` от MAX | `models.py` |

## 📄 Лицензия

MIT

---

## 🔗 Связанные проекты

| Проект | Описание |
|---------|-------------|
| [max-hermes](https://github.com/RuslanStrogov/max-hermes) | Standalone bridge daemon — webhook, Docker, systemd |
| [max-hermes-plugin](https://github.com/RuslanStrogov/max-hermes-plugin) | Native Hermes Agent platform plugin |


---
<div align="center">

  <sub>🇷🇺 Опенсорс — **Поддержи наш продукт** · <a href="https://br-design.ru/">BR-DESIGN</a></sub>

</div>