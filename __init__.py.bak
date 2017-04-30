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
        self.withRegex = ""
        self.forRegex = ""

    def initialize(self):

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
