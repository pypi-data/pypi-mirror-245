# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import logging
import re

import pywikibot
from pywikibot import pagegenerators as pg

from f3wikidatabot.forge import Forge
from f3wikidatabot import plugin

log = logging.getLogger(__name__)


class Features(plugin.Plugin):
    def __init__(self, *args):
        super(Features, self).__init__(*args)

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser(add_help=False)
        return parser

    @staticmethod
    def filter_names():
        return []

    def get_query(self, filter):
        format_args = {
            "instance_of": self.P_instance_of,
            "end_time": self.P_end_time,

            "website": self.Q_website.getID(),
            "forge": self.Q_forge.getID(),
        }
        query = """
         SELECT ?item
         WHERE
         {{
           {{
             ?item wdt:{instance_of} wd:{forge}.
             MINUS {{
                 ?item p:{end_time} ?ignore0. # Do not include items with end time, i.e. forges that are obsolete
             }}
           }}
           FILTER NOT EXISTS {{
             ?item wdt:{instance_of}+ wd:{website}.
           }} # exclude online services running a forge, only keep forge software
         }}
        """.format(
            **format_args
        )
        return query

    def run(self, item):
        self.fixup(item)
        self.verify(item)

    def feature_items(self):
        #
        # For an authoritative list of feature items, see
        # https://www.wikidata.org/wiki/Wikidata:WikiProject_Informatics/Forges#Properties
        #
        return [
            self.Q_repository.getID(),
            self.Q_issue_tracking_system.getID(),
            self.Q_continuous_integration_software.getID(),
            self.Q_code_reviewing_software.getID(),
            self.Q_collaborative_wiki_software.getID(),
            self.Q_electronic_mailing_list_manager.getID(),
            self.Q_software_repository.getID(),
            self.Q_pull_request.getID(),
        ]

    def show(self, item):
        item.get()
        forge = Forge(id=item.getID(),
                      label=item.labels.get("en", "no label"))
        features = self.feature_items()
        for instance_of in item.claims.get(self.P_instance_of, []):
            target = instance_of.getTarget()
            if target.getID() in features:
                forge.features.append(target.labels.get("en", "no label"))
            if target.getID() == self.Q_proprietary_software.getID():
                forge.proprietary = True
        for based_on in item.claims.get(self.P_based_on, []):
            target = based_on.getTarget()
            forge.based_on.append(target.labels.get("en", "no label"))
        self.debug(item, f"show {forge}")
        return forge

    def verify(self, item):
        item.get()

        self.debug(item, "verify")
        status = {}
        for claim in item.claims.get(self.P_instance_of, []):
            pass
        return status

    def fixup(self, item):
        pass
