# -*- mode: python; coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from unittest import mock
import pytest  # noqa # caplog

from f3wikidatabot.bot import Bot
from f3wikidatabot.tests.wikidata import WikidataHelper


class TestBot(object):
    def setup_class(self):
        self.site = WikidataHelper().login()

    def teardown_class(self):
        self.site.logout()

    def test_factory(self):
        Bot.factory(["--verbose"])
        assert logging.getLogger("f3wikidatabot").getEffectiveLevel() == logging.DEBUG

        b = Bot.factory([])
        assert logging.getLogger("f3wikidatabot").getEffectiveLevel() == logging.INFO

        assert len(b.plugins) > 0

        plugin = "License"
        b = Bot.factory(["--verbose", "--plugin=" + plugin])
        assert 1 == len(b.plugins)
        assert plugin == b.plugins[0].__class__.__name__

        b = Bot.factory(
            [
                "--verbose",
                "--plugin=License",
            ]
        )
        assert 1 == len(b.plugins)

    @mock.patch.object(Bot, "run_items")
    @mock.patch.object(Bot, "run_query")
    def test_run(self, m_query, m_items):
        b = Bot.factory([])
        b.run()
        m_query.assert_called_with()
        m_items.assert_not_called()

        m_query.reset_mock()
        m_items.reset_mock()
        b = Bot.factory(["--verbose", "--item=Q1"])
        b.run()
        m_items.assert_called_with()
        m_query.assert_not_called()

    @mock.patch("f3wikidatabot.license.License.run")
    def test_run_items(self, m_run):
        b = Bot.factory(
            [
                "--verbose",
                "--item=Q1",
                "--plugin=License",
            ]
        )
        b.run()
        m_run.assert_called_with(mock.ANY)

    @mock.patch("f3wikidatabot.license.License.run")
    @mock.patch("pywikibot.pagegenerators.WikidataSPARQLPageGenerator")
    def test_run_query_default(self, m_query, m_run):
        b = Bot.factory(
            [
                "--verbose",
                "--plugin=License",
            ]
        )
        m_query.side_effect = "one page"
        b.run()
        m_run.assert_called_with(mock.ANY)

    @mock.patch("f3wikidatabot.license.License.run")
    @mock.patch("pywikibot.pagegenerators.WikidataSPARQLPageGenerator")
    def test_run_query_items(self, m_query, m_run, caplog):
        b = Bot.factory(
            [
                "--verbose",
                "--filter=license-verify",
                "--plugin=License",
            ]
        )
        m_query.side_effect = "one page"
        b.run()

        for record in caplog.records:
            if "running query" in record.message:
                assert "?license" in record.message
