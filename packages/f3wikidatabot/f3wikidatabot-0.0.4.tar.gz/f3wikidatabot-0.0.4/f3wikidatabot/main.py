# SPDX-License-Identifier: GPL-3.0-or-later

from f3wikidatabot import bot


class f3wikidatabot(object):
    def run(self, argv):
        return bot.Bot.factory(argv).run()
