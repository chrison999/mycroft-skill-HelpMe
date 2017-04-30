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

__author__ = 'chrison999'

LOGGER = getLogger(__name__)


class HelpMeSkill(MycroftSkill):
    def __init__(self):
        super(HelpMeSkill, self).__init__(name="HelpMeSkill")

    def initialize(self):
        intent = IntentBuilder("HelpIntent").require(
            "HelpMeKeyword").build()
        self.register_intent(intent, self.help_intent)

        intent = IntentBuilder("SkillsIntent").require(
            "SkillsKeyword").build()
        self.register_intent(intent, self.handle_skills_intent)

        intent = IntentBuilder("CommandsIntent").require(
            "CommandsKeyword").build()
        self.register_intent(intent, self.handle_commands_intent)

    def help_intent(self, message):
        self.speak("Say skill if you want help with a skill or commands if you want help with a command",
            expect_response=True)
        self.expecting_answer = True
        self.counter = 0
        self.choice =  None
        self.asked = False

    def handle_skills_intent(self, message):
        self.speak("Say which skill want help with or list to list the available skills",
            expect_response=True)
        self.expecting_answer = True
        self.counter = 0
        self.choice =  None
        self.asked = False

    def handle_commands_intent(self, message):
        self.speak("Say which command you want help with, or list to list the available commands",
            expect_response=True)
        self.expecting_answer = True
        self.counter = 0
        self.choice =  None
        self.asked = False

    def converse(self, transcript):
        utterance = transcript[0]
        # probably better to call another method inside this so it isnt very crowded
        if self.expecting_answer:
            if "skill" in utterance:
                self.expecting_answer = False
                self.choice = "skill"
                self.counter = 0
                self.asked = True
                self.speak("You said skill")
            elif "command" in utterance:
                self.expecting_answer = False
                self.choice = "command"
                self.counter = 0
                self.speak("You said command")
            elif counter >= 3 or "stop" in utterance:
                self.speak("disabling help")
                self.expecting_answer = False
                self.choice = None
                self.counter = 0
                return False
            else:
                self.speak("try again")
                self.counter += 1
                self.choice = None
                return True

        if self.choice is not None:
            self.speak("what skill you want help for")
            self.asked = True
            self.choice = None
            self.counter = 0
            return True

        if asked:
            # TODO grab skill from utterance
            # TODO check if skill name is a skill or invalid
            if self.choice == "skill":
                self.speak("skill help")
                self.asked = False
                self.counter = 0
                self.choice = None
                return True
            elif self.choice == "command":
                self.speak("command help")
                self.asked = False
                self.counter = 0
                self.choice = None
                return True
            elif counter >= 3 or "stop" in utterance:
                self.speak("disabling help")
                self.asked = False 
                self.counter = 0
                self.choice = None
                return False
        return False

    def stop(self):
        pass

def create_skill():
    return HelpMeSkill()
