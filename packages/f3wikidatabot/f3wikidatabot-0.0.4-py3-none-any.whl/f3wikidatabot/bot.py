# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import logging
import textwrap
import time

import pywikibot
from pywikibot import pagegenerators as pg

from f3wikidatabot import license
from f3wikidatabot import features
from f3wikidatabot.plugin import Plugin

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

plugins = [
    license.License,
    features.Features,
]

name2plugin = dict([(p.__name__, p) for p in plugins])


class Bot(object):
    def __init__(self, args):
        self.args = args
        logging.getLogger("f3wikidatabot").setLevel(self.args.verbose)
        self.site = pywikibot.Site(
            code="wikidata" if not self.args.test else "test",
            fam="wikidata",
            user=self.args.user,
        )
        if self.args.test:
            self.site.throttle.setDelays(writedelay=0)
        if self.args.test:
            self.wikidata_site = pywikibot.Site(code="wikidata", fam="wikidata")
        else:
            self.wikidata_site = None
        self.plugins = []
        for name in self.args.plugin or name2plugin.keys():
            plugin = name2plugin[name]
            self.plugins.append(plugin(self, args))

    @staticmethod
    def get_parser():
        filters = []
        available_plugins = []
        for plugin in plugins:
            filters.extend(plugin.filter_names())
            available_plugins.append(plugin.__name__)
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-v",
            "--verbose",
            action="store_const",
            const=logging.DEBUG,
            default=logging.INFO,
        )
        parser.add_argument(
            "--dry-run", action="store_true", default=None, help="no side effect"
        )
        parser.add_argument(
            "--test",
            action="store_true",
            default=None,
            help="use test.wikidata.org instead of wikidata.org",
        )
        parser.add_argument("--user", default=None, help="wikidata user name")
        parser.add_argument(
            "--plugin",
            default=[],
            choices=available_plugins,
            action="append",
            help="use this plugin instead of all of them (can be repeated)",
        )
        parser.add_argument(
            "--show",
            action="store_true",
            default=None,
            help="show items",
        )
        select = parser.add_mutually_exclusive_group()
        select.add_argument(
            "--filter",
            default="",
            choices=filters,
            help="filter with a pre-defined query",
        )
        select.add_argument(
            "--item",
            default=[],
            action="append",
            help="work on this QID (can be repeated)",
        )
        return parser

    @staticmethod
    def factory(argv):
        parents = [
            Bot.get_parser(),
            Plugin.get_parser(),
        ]
        for plugin in plugins:
            parents.append(plugin.get_parser())
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent(
                """\
            A command-line toolbox for the wikidata Forges project.
            """
            ),
            parents=parents,
        )
        return Bot(parser.parse_args(argv))

    def run(self):
        if len(self.args.item) > 0:
            results = self.run_items()
        else:
            results = self.run_query()
        if self.args.show:
            for result in results:
                print(result.to_json())

    def run_items(self):
        results = []
        for item in self.args.item:
            item = pywikibot.ItemPage(self.site, item, 0)
            for plugin in self.plugins:
                results.append(plugin.run_catch(item))
        return results

    def run_query(self):
        for plugin in self.plugins:
            query = plugin.get_query(self.args.filter)
            if query is not None:
                break
        if query is None:
            query = Plugin(self, self.args).get_query(self.args.filter)
        query = query + " # " + str(time.time())
        log.debug("running query " + query)
        results = []
        for item in pg.WikidataSPARQLPageGenerator(
            query, site=self.site, result_type=list
        ):
            for plugin in self.plugins:
                results.append(plugin.run_catch(item))
        return results
