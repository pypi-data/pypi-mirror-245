# -*- mode: python; coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from unittest import mock
import pywikibot

from f3wikidatabot.bot import Bot
from f3wikidatabot.license import License
from f3wikidatabot.tests.wikidata import WikidataHelper

log = logging.getLogger("f3wikidatabot")


class TestLicense(object):
    def setup_class(self):
        self.site = WikidataHelper().login()

    def teardown_class(self):
        self.site.logout()

    def setup(self):
        self.gpl = "GNU General Public License"
        self.mit = "MIT license"
        self.args = [
            "--license",
            self.gpl,
            "--license",
            self.mit,
        ]

    def test_get_item(self):
        bot = Bot.factory(["--verbose"] + self.args)
        license = License(bot, bot.args)
        redirect = "GPL"
        license.get_names("en")
        canonical_item = license.get_item(self.gpl, "en")
        assert canonical_item == license.get_item(redirect, "en")

        gpl_fr = "Licence publique générale GNU"
        names_fr = license.get_names("fr")
        assert gpl_fr in names_fr
        assert canonical_item == license.get_item(gpl_fr, "fr")

    def test_get_names(self):
        bot = Bot.factory(["--verbose"] + self.args)
        license = License(bot, bot.args)
        redirect = "GPL"
        names = license.get_names("en")
        assert self.gpl in names
        assert redirect in names

        canonical_fr = "Licence publique générale GNU"
        names = license.get_names("fr")
        assert canonical_fr in names
        assert self.gpl in names

    def test_template_parse_license(self):
        bot = Bot.factory(["--verbose"] + self.args)
        license = License(bot, bot.args)
        found = license.template_parse_license(
            "[[GNU GPL#v2]] [[MIT/X11 license|]]", "en"
        )
        assert 2 == len(found)
        for item in found:
            item.get()
            license.debug(item, "FOUND")
            assert item.labels["en"] in (self.gpl, self.mit)

    @mock.patch("f3wikidatabot.license.License.set_license2item")
    @mock.patch("f3wikidatabot.plugin.Plugin.get_sitelink_item")
    def test_fixup(self, m_get_sitelink_item, m_set_license2item):
        bot = Bot.factory(
            [
                "--verbose",
                "--test",
                "--user=F3BotCI",
            ]
        )
        license = License(bot, bot.args)
        gpl = license.Q_GNU_General_Public_License
        gpl.get()
        found = False
        if gpl.claims:
            for claim in gpl.claims.get(license.P_subclass_of, []):
                if claim.type != "wikibase-item":
                    continue
                if claim.getTarget().getID() == license.Q_free_software_license.getID():
                    found = True
                    break
        if not found:
            subclass_of = pywikibot.Claim(license.bot.site, license.P_subclass_of, 0)
            subclass_of.setTarget(license.Q_free_software_license)
            gpl.addClaim(subclass_of)
        gpl.setSitelink({"site": "enwiki", "title": self.gpl})
        gpl.get(force=True)

        emacs = license.Q_GNU_Emacs
        emacs.get()
        if emacs.claims:
            licenses = emacs.claims.get(license.P_license, [])
            if licenses:
                emacs.removeClaims(licenses)
                emacs.get(force=True)

        def set_license2item():
            license.license2item = {self.gpl: license.Q_GNU_General_Public_License}

        m_set_license2item.side_effect = set_license2item

        def get_sitelink_item(dbname):
            if dbname == "enwiki":
                return license.Q_English_Wikipedia
            elif dbname == "frwiki":
                return license.Q_French_Wikipedia
            else:
                assert 0, "unexpected " + dbname

        m_get_sitelink_item.side_effect = get_sitelink_item
        emacs.removeSitelinks(["enwiki"])
        emacs.removeSitelinks(["frwiki"])
        emacs.get(force=True)
        assert ["nothing"] == license.fixup(emacs)

        emacs.setSitelink({"site": "enwiki", "title": "GNU Emacs"})
        emacs.setSitelink({"site": "frwiki", "title": "GNU Emacs"})
        emacs.get(force=True)
        assert [self.gpl] == license.fixup(emacs)


# Local Variables:
# compile-command: "cd .. ; tox -e py3 tests/test_license.py"
# End:
