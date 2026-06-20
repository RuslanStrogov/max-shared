"""Tests for max-shared converter."""

import pytest
from max_shared.converter import MessageConverter
from max_shared.models import (
    MAXUpdate,
    MAXMessage,
    MAXUser,
    MAXRecipient,
    MAXMessageBody,
    MAXAttachment,
    MAXAttachmentPayload,
    UpdateType,
)


def _make_message(
    text: str = "hello",
    user_id: int = 123,
    chat_id: int = 456,
    user_name: str = "Test",
    chat_type: str = "dialog",
    attachments: list = None,
) -> MAXMessage:
    return MAXMessage(
        sender=MAXUser(user_id=user_id, name=user_name),
        recipient=MAXRecipient(chat_id=chat_id, chat_type=chat_type),
        body=MAXMessageBody(
            text=text,
            mid="msg_1",
            attachments=attachments or [],
        ),
        timestamp=1000,
    )


class TestMessageConverter:
    def test_message_created(self):
        msg = _make_message(text="hello world")
        update = MAXUpdate(
            update_type=UpdateType.MESSAGE_CREATED,
            message=msg,
            timestamp=1000,
        )
        result = MessageConverter.max_update_to_message(update)
        assert result is not None
        assert result["message"] == "hello world"
        assert result["user_id"] == "123"
        assert result["chat_id"] == "456"
        assert result["platform"] == "max"

    def test_bot_started(self):
        msg = _make_message()
        update = MAXUpdate(
            update_type=UpdateType.BOT_STARTED,
            message=msg,
            timestamp=1000,
        )
        result = MessageConverter.max_update_to_message(update)
        assert result is not None
        assert result["message"] == "/start"

    def test_unsupported_type_returns_none(self):
        update = MAXUpdate(
            update_type=UpdateType.CHAT_TITLE_CHANGED,
            timestamp=1000,
        )
        # CHAT_TITLE_CHANGED without message returns empty payload, not None
        result = MessageConverter.max_update_to_message(update)
        assert result is not None
        assert result["message"] == "[Название чата изменено]"

    def test_response_to_max_message(self):
        response = {"message": "Hello **world**"}
        result = MessageConverter.response_to_max_message(
            response, user_id=123
        )
        assert result["text"] == "Hello **world**"
        assert result["user_id"] == 123
        assert result.get("format") == "markdown"

    def test_response_plain_text_no_markdown(self):
        response = {"message": "Hello world"}
        result = MessageConverter.response_to_max_message(
            response, chat_id=456
        )
        assert result["chat_id"] == 456
        assert "format" not in result

    def test_determine_reply_target_dialog(self):
        sender = MAXUser(user_id=123, name="Test")
        recipient = MAXRecipient(chat_id=456, chat_type="dialog")
        chat_id, user_id = MessageConverter.determine_reply_target(
            recipient, sender
        )
        assert user_id == 123
        assert chat_id is None

    def test_determine_reply_target_group(self):
        sender = MAXUser(user_id=123, name="Test")
        recipient = MAXRecipient(chat_id=456, chat_type="group")
        chat_id, user_id = MessageConverter.determine_reply_target(
            recipient, sender
        )
        assert chat_id == 456
        assert user_id is None

    def test_build_inline_keyboard(self):
        buttons = [[{"type": "callback", "text": "OK", "payload": "ok"}]]
        result = MessageConverter.build_inline_keyboard(buttons)
        assert result["type"] == "inline_keyboard"
        assert result["payload"]["buttons"] == buttons
