# SPDX-License-Identifier: GPL-3.0-or-later

import random
import string

import pywikibot
from pywikibot.login import ClientLoginManager


class WikidataHelper(object):
    def login(self):
        site = pywikibot.Site("test", "wikidata", "F3BotCI")
        ClientLoginManager(
            site=site, user="F3BotCI", password="quars3Knafs5"
        ).login_to_site()
        return site

    @staticmethod
    def random_name():
        return "".join(random.choice(string.ascii_lowercase) for _ in range(16))
