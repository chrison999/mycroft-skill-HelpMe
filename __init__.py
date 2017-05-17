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

LOGGER = getLogger(__name__)


class HelpMeSkill(MycroftSkill):
    def __init__(self):
        super(HelpMeSkill, self).__init__(name="HelpMeSkill")
        self.withRegex = ""
        self.forRegex = ""
        self.help_files = {} #skill_folder : help_json dict

    def initialize(self):
        self.layers = IntentLayers(self.emitter)
        self.build_intents()
        self.build_layers()
        self.build_help()

    def build_help(self)
        SKILLS_DIR = dirname(dirname(__file__))
        # Scan the folder that contains Skills.
        list = filter(lambda x: os.path.isdir(
            os.path.join(SKILLS_DIR, x)), os.listdir(SKILLS_DIR))
        # see if help file exists
        for skill_folder in list:
            path = os.path.join(SKILLS_DIR, skill_folder)
            print path
            # checking if help exists
            if not "help.json" in os.listdir(path):
                # create help file
                help = {}
                help["skill_name"] = skill_folder.lower().replace("_"," ").replace("-"," ").replace("mycroft","").replace("skill","")
                help["description"] = "no description provided for this skill"
                # TODO try to get github repo for website
                help["support"] = {"email":"not provided", "website":"not provided"}
                help["commands"] = {} #command : "description of what command does"
                self.help_files.setdefault(skill_folder, help)
            else:
                # load help file
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


# this could just be imported, im redefining it here for now until other skills can be made as requirements in install


class IntentLayers():
    def __init__(self, emitter, layers = [], timer = 500):
        self.emitter = emitter
        # make intent tree for N layers
        self.layers = []
        self.current_layer = 0
        self.timer = timer
        self.timer_thread = None
        for layer in layers:
            self.add_layer(layer)
        self.activate_layer(0)

    def disable_intent(self, intent_name):
        """Disable a registered intent"""
        self.emitter.emit(Message("disable_intent", {"intent_name": intent_name}))

    def enable_intent(self, intent_name):
        """Reenable a registered self intent"""
        self.emitter.emit(Message("enable_intent", {"intent_name": intent_name}))

    def start_timer(self):

        self.stop_timer()

        # set new timer
        def timer():
            logger.info("New Timer Started")
            start_time = time()
            while time() - start_time <= self.timer:
                sleep(1)
            # on end of timer reset tree
            logger.info("Timer Ended - resetting tree")
            self.reset()

        self.timer_thread = Process(target=timer)
        self.timer_thread.start()

    def stop_timer(self):
        logger.info("Stopping previous timer")
        try:
            # cancel previous timers
            self.timer_thread.terminate()
        except:
            pass

    def reset(self):
        logger.info("Reseting Tree")
        self.stop_timer()
        self.activate_layer(0)

    def next(self):
        logger.info("Going to next Tree Layer")
        self.current_layer += 1
        if self.current_layer > len(self.layers):
            logger.info("Already in last layer, going to layer 0")
            self.current_layer = 0
        if self.current_layer != 0:
            self.start_timer()
        self.activate_layer(self.current_layer)

    def previous(self):
        logger.info("Going to previous Tree Layer")
        self.current_layer -= 1
        if self.current_layer < 0:
            self.current_layer = len(self.layers)
            logger.info("Already in layer 0, going to last layer")
        if self.current_layer != 0:
            self.start_timer()
        self.activate_layer(self.current_layer)

    def add_layer(self, intent_list=[]):
        self.layers.append(intent_list)
        logger.info("Adding layer to tree " + str(intent_list))

    def replace_layer(self, layer_num, intent_list=[]):
        logger.info("Removing layer number " + str(layer_num) + " from tree ")
        self.layers.pop(layer_num)
        self.layers[layer_num] = intent_list
        logger.info("Adding layer" + str(intent_list) + " to tree in position " + str(layer_num) )

    def remove_layer(self, layer_num):
        self.layers.pop(layer_num)
        logger.info("Removing layer number " + str(layer_num) + " from tree ")

    def find_layer(self, intent_list=[]):
        layer_list = []
        for i in range(0, len(self.layers)):
            if self.layers[i] == intent_list:
                layer_list.append(i)
        return layer_list

    def disable(self):
        logger.info("Disabling intent layers")
        # disable all tree layers
        for i in range(0, len(self.layers)):
            self.deactivate_layer(i)

    def activate_layer(self, layer_num):
        # error check
        if layer_num < 0 or layer_num > len(self.layers):
            logger.error("invalid layer number")
            return

        self.current_layer = layer_num

        # disable other layers
        self.disable()

        # TODO in here we should wait for all intents to be detached
        # sometimes detach intent from this step comes after register from next
        sleep(0.3)

        # enable layer
        logger.info("Activating Layer " + str(layer_num))
        for intent_name in self.layers[layer_num]:
            self.enable_intent(intent_name)

    def deactivate_layer(self, layer_num):
        # error check
        if layer_num < 0 or layer_num > len(self.layers):
            logger.error("invalid layer number")
            return
        logger.info("Deactivating Layer " + str(layer_num))
        for intent_name in self.layers[layer_num]:
            self.disable_intent(intent_name)

# TODO intent layer usage / stats / help skill
