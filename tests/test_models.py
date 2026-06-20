"""Tests for max-shared models."""

import pytest
from max_shared.models import (
    MAXUser,
    MAXRecipient,
    MAXAttachment,
    MAXUpdate,
    UpdateType,
)


class TestMAXUser:
    def test_display_name_from_name(self):
        user = MAXUser(user_id=1, name="Ruslan")
        assert user.display_name == "Ruslan"

    def test_display_name_from_parts(self):
        user = MAXUser(user_id=1, first_name="Ruslan", last_name="Strogov")
        assert user.display_name == "Ruslan Strogov"

    def test_display_name_fallback(self):
        user = MAXUser(user_id=1)
        assert user.display_name == "Unknown"


class TestMAXRecipient:
    def test_is_group(self):
        r = MAXRecipient(chat_id=1, chat_type="group")
        assert r.is_group

    def test_is_dialog(self):
        r = MAXRecipient(chat_id=1, chat_type="dialog")
        assert not r.is_group


class TestMAXAttachment:
    def test_is_media_image(self):
        a = MAXAttachment(type="image")
        assert a.is_media

    def test_is_media_video(self):
        a = MAXAttachment(type="video")
        assert a.is_media

    def test_is_file(self):
        a = MAXAttachment(type="file")
        assert a.is_file

    def test_not_media(self):
        a = MAXAttachment(type="inline_keyboard")
        assert not a.is_media
