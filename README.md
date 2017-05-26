# mycroft-skill-HelpMe

A skill for MycroftAI that implements an internal help facility

## DESCRIPTION:

This Mycroft skill implements an internal help facility such that
the user can obtain help on how to operate Mycroft and any skills.

## OUTPUT

        Input: help me with jokeskill
        2017-05-26 17:42:30,332 - CLIClient - INFO - Speak: I can help you with the following things. 1 - Description of this skill,  2 - Intent Description, 3 - Commands for this skill, 4 - Contact

        Input: help me with commands
        2017-05-26 17:42:35,531 - CLIClient - INFO - Speak: Keywords for JokingIntent
        2017-05-26 17:42:35,532 - CLIClient - INFO - Speak: JokingKeyword can be triggered by the following sentences, joke, make me laugh, brighten my day, tell me joke,

        Input: help me with intents
        2017-05-26 17:42:45,122 - CLIClient - INFO - Speak: The following intents are available
        2017-05-26 17:42:45,127 - CLIClient - INFO - Speak: JokingIntent, , to activate this intent you can use the following keywords JokingKeyword,

        Input: help me with skill
        2017-05-26 17:42:52,210 - CLIClient - INFO - Speak: skill_joke , no description provided for this skill.


## CURRENT STATE:

Under development.

- auto generates help for all skills
- read help from file
- missing interactive dialog
- poor skill name matching, perhaps use fuzzy match?

Requires [PR#756](https://github.com/MycroftAI/mycroft-core/pull/756) to

- add help skill to priority skills in order to not miss register_intent messages
- get loaded skills from main (for skill name and id)

Will most likely use IntentChains and [Converse method](https://github.com/MycroftAI/mycroft-core/pull/783) for dialog state


generated help files contain

        intents this skill triggers, required leywords and placeholder description of each intent,
        utterances that correspond to each keyword, #TODO regex
        github link, author name (from github link), placeholder contact field
        placeholder skill description
        skill name


## USAGE:

To initial this skill, the user will utter any of the following keywords:

- help me with skill_name <- will give options for help about this skill <- do this before other commands!
- help me with skill <- info about previous skill
- help me with commands <- info about previous skill's commands/ keywords
- help me with intents <- info about previous skill's intents


More functions and keywords will be implemented in the near future.

##### NOTE:

This skill is a _*prototype*_ of how a full-featured help facility
might be implemented in Mycroft.  Comments and suggestions for
improvements are welcome by emailing me at chrison999 (AT) yahoo.ca.
 