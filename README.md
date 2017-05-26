# mycroft-skill-HelpMe

A skill for MycroftAI that implements an internal help facility

## DESCRIPTION:

This Mycroft skill implements an internal help facility such that
the user can obtain help on how to operate Mycroft and any skills.

## CURRENT STATE:

Under development. Requires https://github.com/MycroftAI/mycroft-core/pull/756

- auto generates help for all skills
- read help from file
- missing interactive dialog



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
 