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
from mycroft.messagebus.message import Message
import os
import json
import subprocess
from os.path import dirname
from time import time , sleep

__authors__ = ['chrison999', "jarbas"]

logger = getLogger(__name__)

SKILLS_DIR = dirname(dirname(__file__))


class HelpMeSkill(MycroftSkill):
    def __init__(self):
        super(HelpMeSkill, self).__init__(name="HelpMeSkill")
        self.reload_skill = False
        self.help_files = {} #skill_folder : help_json dict
        self.loaded_skills = []  # [{"name":skill_name, "id":skill_id, "folder":skill_folder}] #if name = unloaded <- blacklisted or shutdown
        self.time_out = 5

    def initialize(self):
        self.emitter.on("register_vocab", self.handle_regex)
        self.emitter.on("register_intent", self.handle_intent)
        self.emitter.on("loaded_skills_response", self.handle_receive_loaded_skills)
        self.get_loaded_skills()
        #self.layers = IntentLayers(self.emitter)
        self.build_intents()
        self.build_layers()
        self.build_help()
        intent = IntentBuilder("HelpWithIntent").require("HelpMeKeyword").require("SkillName").build()
        self.register_intent(intent, self.handle_help_me_with_intent)

    def handle_help_me_with_intent(self, message):
        skill = message.data["SkillName"]
        help = self.get_skill_help(skill)
        if help is None:
            self.speak("no skill")
        else:
            for k in help:
                print k, help[k]

    def get_loaded_skills(self):
        # asks main for loaded skill names, ids
        self.emitter.emit(Message("loaded_skills_request", {}))
        self.waiting = True
        start_time = time()
        t = 0
        while self.waiting and t < self.time_out:
            t = time() - start_time
            sleep(0.1)
        self.waiting = False

    def handle_receive_loaded_skills(self, message):
        self.loaded_skills = message.data["skills"]
        self.skill_name_to_id = {}
        for skill in self.loaded_skills:
            self.skill_name_to_id[skill["name"].lower().replace("_", " ").replace(" skill", "").replace("skill", "")] = skill["id"]
        self.waiting = False

    def handle_intent(self, message):
        keys = message.data["requires"]
        keywords = []
        for word in keys:
            keywords.append(word[0])
        skill_id, intent_name = message.data["name"].split(":")
        intent_data = {"intent_name": intent_name, "intent_keywords": keywords, "intent_description": "no description provided"}
        for skill in self.loaded_skills:
            if skill["id"] == int(skill_id):
                if intent_data not in self.help_files[skill["folder"]]["intents"]:
                    self.help_files[skill["folder"]]["intents"].append(intent_data)

    def handle_regex(self, message):
        regex = message.data["regex"]
        if regex is None:
            return
        # TODO process regex
        #print regex

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

    def get_possible_skill_names(self, name):
        # try to make a ugly string into something pronounceable the user could have said
        possible_names = [name.lower()]
        # replace _ and - with spaces -> "Skill_HelpMe" becomes "Skill HelpMe"
        name = name.replace("_", " ").replace("-", " ")
        if name not in possible_names:
            possible_names.append(name)
        # put spaces wherever a big-case letter is found -> "Skill Help Me"
        i = 0
        for char in name:
            if char.isupper() and i>0:
                name = name[:i] + " " + name[i:]
            i +=1
        if name not in possible_names:
            possible_names.append(name)
        # make lower -> "skill help me"
        name = name.lower()
        if name not in possible_names:
            possible_names.append(name)
        # replace "skill" -> " help me"
        name = name.replace("skill", "")
        if name not in possible_names:
            possible_names.append(name)
        # if first or last char in string is " " remove -> "help me"
        if name[0] == " ":
            name = name[1:]
            if name not in possible_names:
                possible_names.append(name)
        if name[-1] == " ":
            name = name[:len(name)-1]
            if name not in possible_names:
                possible_names.append(name)
        return possible_names

    def get_skill_help(self, skill_string):
        # this trys to manipulate the extracted string from regex and check against help files
        # folders can be any combinations of uppercase lower case and can even have underscores or "skill" in the name
        # this opens several possibilities of utterances that could be in regex asking for the skill
        # check if id was provided get help directly, this most likely won't happen
        if skill_string.isdigit():
            for skill in self.loaded_skills:
                if skill["id"] == int(skill_string):
                    return self.help_files[skill["folder"]]

        # process the string for common name possibilities to try
        possible_names = self.get_possible_skill_names(skill_string)
        for possible_name in possible_names:
            # if the provided name matches a skill folder use it
            if possible_name in self.help_files.keys():
                return self.help_files[possible_name]

        # process all skills folder names to be more pronounceable and see if they match this skill
        for skill in self.loaded_skills:
            possible_folders = self.get_possible_skill_names(skill["folder"])

            for possible_name2 in possible_folders:
                if possible_name2 in possible_names:
                    return self.help_files[skill["folder"]]

        # process all skills internal names to make more pronounceable see if they match this skill
        for skill in self.loaded_skills:
            if skill["name"] == "unloaded":
                continue
            p = self.get_possible_skill_names(skill["name"])
            for possible_name2 in p:
                if possible_name2 in possible_names:
                    return self.help_files[skill["folder"]]
        # TODO return some error, skill is not available most likely, maybe do some fuzzy matching for best option?

    def generate_basic_help(self, skill_folder):
        # this generates basic help files with all the info it can get from the skill folder
        path = os.path.join(SKILLS_DIR, skill_folder)
        help = {}
        # Try to get name from loaded skills manifest
        name = "unloaded"
        for skill in self.loaded_skills:
            if skill["folder"] == skill_folder:
                name = skill["name"]
        if name == "unloaded":
            # turn folder name into a more user friendly / pronounceble name
            help["skill_name"] = skill_folder.lower().replace("_", " ").replace("-", " ").replace("mycroft", "").replace("skill", "")
            if help["skill_name"][0] == " ":
                help["skill_name"] = help["skill_name"][1:]
        else:
            help["skill_name"] = name
        help["description"] = "no description provided for this skill"
        try:
            website = subprocess.check_output(["git", "remote", "-v"], cwd=path)
            website = website.replace("origin\t", "").replace(" (fetch)", "").split("\n")[0]
            author = website.replace("https://github.com/", "")
            author = author[:author.find("/")]
        except:
            website = "not provided"
            author = "unknown"
        help["author"] = author
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
        # make intents
        pass

    def stop(self):
        pass


def create_skill():
    return HelpMeSkill()

