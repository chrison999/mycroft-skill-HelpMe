# Copyright 2017 Chris O'Neill (chrison999)
#
# This Mycroft skill is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This Mycroft skill is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along this skill.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import os
from os.path import dirname
__author__ = 'chrison999'

logger = getLogger(__name__)


class HelpMeSkill(MycroftSkill):
    def __init__(self):
        super(HelpMeSkill, self).__init__(name="HelpMeSkill")
        self.withRegex = ""
        self.forRegex = ""
        self.help_files = {} #skill_folder : help_json dict

    def initialize(self):
        #self.layers = IntentLayers(self.emitter)
        self.build_intents()
        self.build_layers()
        self.build_help()

    def build_help(self):
        SKILLS_DIR = dirname(dirname(__file__))
        # Scan the folder that contains Skills.
        list = filter(lambda x: os.path.isdir(
            os.path.join(SKILLS_DIR, x)), os.listdir(SKILLS_DIR))
        # see if help file exists
        for skill_folder in list:
            path = os.path.join(SKILLS_DIR, skill_folder)
            # checking if help exists
            if "help.json" not in os.listdir(path):
                # create help file
                help = {}
                help["skill_name"] = skill_folder.lower().replace("_"," ").replace("-"," ").replace("mycroft","").replace("skill","")
                help["description"] = "no description provided for this skill"
                # TODO try to get github repo for website
                help["support"] = {"email":"not provided", "website":"not provided"}
                help["commands"] = {}  # command : "description of what command does"
                # get path for this skills vocab
                cpath = path + "/vocab/" + self.lang
                # check if vocab files were defined for this skill
                if os.path.exists(cpath):
                    # list of vocab files
                    list = filter(lambda x: os.path.isfile(
                        os.path.join(cpath, x)), os.listdir(cpath))
                    for v in list:
                        vpath = cpath + "/" + v
                        # read each command from each vocab file
                        with open(vpath, 'r') as voc_file:
                            for line in voc_file.readlines():
                                parts = line.strip().split("|")
                                entity = parts[0]
                                help["commands"].setdefault(entity, "")
                # TODO get regex commands
                self.help_files.setdefault(skill_folder, help)
                # TODO save help.json in skill folder
            else:
                # TODO load help file
                self.help_files.setdefault(skill_folder, {})

    def build_layers(self):
        # activate different intents depending on query
        pass

    def build_intents(self):
        # Intent for no regexs triggered

        help_me_intent = IntentBuilder("HelpMeIntent"). \
            require("HelpMeKeyword").build()
        self.register_intent(help_me_intent, self.handle_help_me_intent)

        # Intent for withRexex triggered

        intent = IntentBuilder("withRegexIntent").require("HelpMeKeyword") \
            .optionally("withRegex").build()
        self.register_intent(intent, self.handle_withRegex_intent)

        # Intent for forRexex triggered

        intent = IntentBuilder("forRegexIntent").require("HelpMeKeyword") \
            .optionally("forRegex").build()
        self.register_intent(intent, self.handle_forRegex_intent)

    # No regex triggered

    def handle_help_me_intent(self, message):
        self.speak_dialog("help.me")

    # withRegex triggered

    def handle_withRegex_intent(self, message):
        self.withRegex = str(message.data.get("withRegex"))  # optional parameter
        self.forRegex = str(message.data.get("forRegex"))  # optional parameter
        if self.forRegex == 'None':
            self.speak("no for regex")
        else:
            self.speak(self.forRegex)
        self.speak_dialog('help.me.withRegex', {'withRegex': self.withRegex})

    # forRegex triggered

    def handle_forRegex_intent(self, message):
        self.forRegex = str(message.data.get("forRegex"))  # optional parameter
        self.speak_dialog("help.me.forRegex")

    def stop(self):
        pass


def create_skill():
    return HelpMeSkill()

