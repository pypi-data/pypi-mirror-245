# -*- mode: python; coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import date
import logging

import pytest
import pywikibot
import time

from f3wikidatabot.bot import Bot
from f3wikidatabot.plugin import Plugin
from f3wikidatabot.tests.wikidata import WikidataHelper

log = logging.getLogger("f3wikidatabot")


class TestPlugin(object):
    def setup_class(self):
        self.site = WikidataHelper().login()

    def teardown_class(self):
        self.site.logout()

    def test_lookup_item(self):
        bot = Bot.factory(
            [
                "--test",
                "--user=F3BotCI",
                "--verbose",
            ]
        )
        plugin = Plugin(bot, bot.args)
        assert 0 == len(plugin.bot.entities["item"])

        git = plugin.Q_git
        assert 1 == len(plugin.bot.entities["item"])
        assert git == plugin.Q_git
        assert plugin.Q_Concurrent_Versions_System
        assert 2 == len(plugin.bot.entities["item"])

    def test_create_entity(self):
        bot = Bot.factory(
            [
                "--test",
                "--user=F3BotCI",
                "--verbose",
            ]
        )
        plugin = Plugin(bot, bot.args)
        name = "Q_" + WikidataHelper.random_name()
        log.debug(f"looking for {name}")
        item = plugin.__getattribute__(name)
        assert 1 == len(plugin.bot.entities["item"])

        plugin.clear_entity_label(item.getID())
        assert 0 == len(plugin.bot.entities["item"])

        item = plugin.__getattribute__(name)
        assert 1 == len(plugin.bot.entities["item"])

        log.debug(f"moving to property2datatype")

        #
        # These properties must exist in wikidata.org and are used to create the same
        # property in test.wikidata.org
        #
        property2datatype = {
            "P_source_code_repository_URL": "url",
            "P_chemical_formula": "string",
            "P_based_on": "wikibase-item",
        }

        wikidata_bot = Bot.factory(
            [
                "--user=F3BotCI",
                "--verbose",
            ]
        )
        wikidata_plugin = Plugin(wikidata_bot, wikidata_bot.args)
        for attr, datatype in property2datatype.items():
            log.debug(f"looking for {name} datatype {datatype}")
            plugin.reset_cache()
            #
            # because plugin uses test.wikidata.org (--test), it will
            # create the property if it does not exist already. It would
            # fail if it was wikidata.org because this is not allowed.
            #
            property = plugin.__getattribute__(attr)
            assert 1 == len(plugin.bot.entities["property"])
            #
            # clear the property label so it can no longer be found
            #
            plugin.clear_entity_label(property)
            assert 0 == len(plugin.bot.entities["property"])
            #
            # retry because the change is asynchronous and the property
            # may still have the label that allows to find it for a short
            # while
            #
            for _ in range(120):
                if plugin.lookup_entity(attr, type="property") is None:
                    break
                log.debug(f"retry lookup_entity: {attr}")
            #
            # this will fail to find the property and re-create it
            #
            property = plugin.__getattribute__(attr)
            assert 1 == len(plugin.bot.entities["property"])

            #
            # verify that the property created in test.wikidata.org has the
            # same type as the property that exists in wikidata.org
            #
            new_content = plugin.bot.site.loadcontent({"ids": property}, "datatype")
            wikidata_property = wikidata_plugin.__getattribute__(attr)
            wikidata_content = wikidata_plugin.bot.site.loadcontent(
                {"ids": wikidata_property}, "datatype"
            )
            assert (
                wikidata_content[wikidata_property]["datatype"]
                == new_content[property]["datatype"]
            ), attr
            assert datatype == wikidata_content[wikidata_property]["datatype"], attr

    def test_set_retrieved(self):
        bot = Bot.factory(
            [
                "--test",
                "--user=F3BotCI",
            ]
        )
        plugin = Plugin(bot, bot.args)
        item = plugin.__getattribute__("Q_" + WikidataHelper.random_name())
        claim = pywikibot.Claim(plugin.bot.site, plugin.P_source_code_repository_URL, 0)
        claim.setTarget("http://repo.com/some")
        item.addClaim(claim)
        plugin.set_retrieved(item, claim)
        assert plugin.need_verification(claim) is False

        plugin.set_retrieved(item, claim, date(1965, 11, 2))
        assert plugin.need_verification(claim) is True

        plugin.clear_entity_label(item.getID())

    def test_search_entity(self):
        bot = Bot.factory(
            [
                "--test",
                "--user=F3BotCI",
                "--verbose",
            ]
        )
        plugin = Plugin(bot, bot.args)
        # ensure space, - and _ are accepted
        name = WikidataHelper.random_name() + "-some thing_else"

        #
        # Insert two items that have the same label. Then search for
        # the label and check that it throws an exception. Having two
        # items with the same label is a source of confusion and needs
        # manual fixing.
        #
        first = plugin.bot.site.editEntity({"new": "item"}, {})
        first_entity = plugin.set_entity_label(first["entity"]["id"], name)
        second = plugin.bot.site.editEntity({"new": "item"}, {})
        second_entity = plugin.set_entity_label(second["entity"]["id"], name)

        assert first["entity"]["id"] != second["entity"]["id"]

        with pytest.raises(ValueError) as e:
            for _ in range(120):
                #
                # It takes time for test.wikidata.org to return
                # **both** items in the search (wbsearchentities API
                # endpoint), wait for it.
                #
                plugin.search_entity(plugin.bot.site, name, type="item")
                time.sleep(5)
        assert "found multiple items" in str(e.value)

        #
        # Special case implemented by plugin.search_entity. If an item
        # is an instance of a disambiguation page, it is not returned
        # in the search results.
        #
        claim = pywikibot.Claim(plugin.bot.site, plugin.P_instance_of, 0)
        claim.setTarget(plugin.Q_Wikimedia_disambiguation_page)
        first_entity.addClaim(claim)

        found = plugin.search_entity(bot.site, name, type="item")
        assert found.getID() == second_entity.getID()

        third = plugin.bot.site.editEntity({"new": "item"}, {})
        third_entity = plugin.set_entity_label(third["entity"]["id"], name)

        with pytest.raises(ValueError) as e:
            for _ in range(120):
                #
                # It takes time for test.wikidata.org to return
                # **both** items in the search (wbsearchentities API
                # endpoint), wait for it.
                #
                plugin.search_entity(plugin.bot.site, name, type="item")
                time.sleep(5)
        assert "found multiple items" in str(e.value)

        Plugin.authoritative["test"][name] = second_entity.getID()
        found = plugin.search_entity(plugin.bot.site, name, type="item")
        assert found.getID() == second_entity.getID()

    def test_get_template_field(self):
        bot = Bot.factory(["--verbose"])
        plugin = Plugin(bot, bot.args)
        item = plugin.Q_GNU_Emacs
        expected = {
            "simple": "ignore",
            "nl": "ignore",
            "en": "ignore",
        }
        item.get()
        lang2field = {"en": "License"}
        lang2pattern = {"*": "Infobox"}
        actual = plugin.get_template_field(item, lang2field, lang2pattern)
        assert actual.keys() == expected.keys()

    def test_translate_title(self):
        bot = Bot.factory(["--verbose"])
        plugin = Plugin(bot, bot.args)
        assert "Licence" == plugin.translate_title("License", "fr")
        assert plugin.translate_title("License", "??") is None

    def test_get_redirects(self):
        bot = Bot.factory(["--verbose"])
        plugin = Plugin(bot, bot.args)
        titles = plugin.get_redirects("GNU General Public License", "en")
        assert "GPL" in titles

    def test_get_sitelink_item(self):
        bot = Bot.factory(["--verbose"])
        plugin = Plugin(bot, bot.args)
        enwiki = plugin.get_sitelink_item("enwiki")
        assert "English Wikipedia" == enwiki.labels["en"]

        frwiki = plugin.get_sitelink_item("frwiki")
        assert "French Wikipedia" == frwiki.labels["en"]
