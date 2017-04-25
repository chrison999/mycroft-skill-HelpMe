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
        help_me_intent = IntentBuilder("HelpMeIntent"). \
            require("HelpMeKeyword").build()
        self.register_intent(help_me_intent, self.handle_help_me_intent)

    def handle_help_me_intent(self, message):
        self.speak_dialog("help.me")

    def stop(self):
        pass


def create_skill():
    return HelpMeSkill()
