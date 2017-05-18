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
import json
import subprocess
from os.path import dirname
__author__ = 'chrison999'

logger = getLogger(__name__)

SKILLS_DIR = dirname(dirname(__file__))

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

    def build_help(self, reset=True):
        # Scan the folder that contains Skills.
        list = filter(lambda x: os.path.isdir(
            os.path.join(SKILLS_DIR, x)), os.listdir(SKILLS_DIR))
        for skill_folder in list:
            # generate basic help
            self.help_files[skill_folder] = self.generate_basic_help(skill_folder)
            path = os.path.join(SKILLS_DIR, skill_folder)
            if "help.json" not in os.listdir(path) or reset:
                # if help not in dir, save generated help
                self.save_help(skill_folder)
            else:
                # if help.json is in dir read it
                help = self.read_help(skill_folder)
                # TODO merge missing fields instead of over-writing
                self.help_files[skill_folder] = help

            print self.help_files[skill_folder]

    def generate_basic_help(self, skill_folder):
        # this generates basic help files with all the info it can get from the skill folder
        path = os.path.join(SKILLS_DIR, skill_folder)
        help = {}
        help["skill_name"] = skill_folder.lower().replace("_", " ").replace("-", " ").replace("mycroft",
                                                                                              "").replace(
            "skill", "")
        if help["skill_name"][0] == " ":
            help["skill_name"] = help["skill_name"][1:]
        help["description"] = "no description provided for this skill"
        try:
            website = subprocess.check_output(["git", "remote", "-v"], cwd=path)
            website = website.replace("origin\t", "").replace(" (fetch)", "").split("\n")[0]
        except:
            website = "not provided"
        help["support"] = {"email": "not provided", "website": website}
        help["keywords"] = {}  # keyword : "utterance"
        help["intents"] = [] #{"intent_name":name, "intent_decription":desceiption, "intent_keywords":[keyword list]}
        # get path for this skills vocab
        cpath = path + "/vocab/" + self.lang
        # check if vocab files were defined for this skill
        if os.path.exists(cpath):
            # list of vocab files
            list = filter(lambda x: os.path.isfile(
                os.path.join(cpath, x)), os.listdir(cpath))
            for v in list:
                vpath = cpath + "/" + v
                v = v.replace(".voc", "")
                help["keywords"].setdefault(v, [])
                # read each command from each vocab file
                with open(vpath, 'r') as voc_file:
                    for line in voc_file.readlines():
                        parts = line.strip().split("|")
                        entity = parts[0]
                        if entity != "" and entity != " ":
                            help["keywords"][v].append(entity)
            return help

    def read_help(self, skill_folder):
        # read help.json from this skill folder
        with open(SKILLS_DIR + "/" + skill_folder + "/help.json", 'r') as myfile:
            file_content = myfile.read()
            help = json.loads(file_content)
        return help

    def save_help(self, skill_folder):
        # save help.json in memory to skill folder
        with open(SKILLS_DIR + "/" + skill_folder + "/help.json", 'w') as myfile:
            file_content = self.help_files[skill_folder]
            help = json.dumps(file_content)
            myfile.write(help)
            myfile.close()

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

