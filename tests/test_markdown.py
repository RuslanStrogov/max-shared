"""Tests for max-shared markdown utilities."""

import pytest
from max_shared.markdown import has_markdown, strip_markdown


class TestHasMarkdown:
    def test_plain_text(self):
        assert not has_markdown("Hello world")

    def test_bold(self):
        assert has_markdown("**bold text**")

    def test_italic(self):
        assert has_markdown("*italic text*")

    def test_strikethrough(self):
        assert has_markdown("~~strikethrough~~")

    def test_link(self):
        assert has_markdown("[link](https://example.com)")

    def test_code(self):
        assert has_markdown("`code`")

    def test_header(self):
        assert has_markdown("# Header")

    def test_blockquote(self):
        assert has_markdown("> quote")

    def test_list(self):
        assert has_markdown("- item")

    def test_mixed(self):
        assert has_markdown("Hello **world** and *stuff*")


class TestStripMarkdown:
    def test_bold(self):
        assert strip_markdown("**bold**") == "bold"

    def test_italic(self):
        assert strip_markdown("*italic*") == "italic"

    def test_link(self):
        assert strip_markdown("[text](url)") == "text"

    def test_plain(self):
        assert strip_markdown("plain text") == "plain text"
