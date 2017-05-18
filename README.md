# mycroft-skill-HelpMe

A skill for MycroftAI that implements an internal help facility

## DESCRIPTION:

This Mycroft skill implements an internal help facility such that
the user can obtain help on how to operate Mycroft and any skills.

## CURRENT STATE:

Under development. Requires https://github.com/MycroftAI/mycroft-core/pull/756 , this skill should be a priority skill to laod first and catch all register intent_messages, it also uses the loaded skills manifest function from that PR

- auto generates help for all skills with available info
- read help from file

generated help files contain, 
- intents this skill triggers, required leywords and placeholder description of each intent, 
- utterances that correspond to each keyword, #TODO regex
- github link, author name (from github link), placeholder contact field
- placeholder skill description
- skill name

## USAGE:

To initial this skill, the user will utter any of the following keywords:

  * "Mycroft, help"
  * "Mycroft, help me"

More functions and keywords will be implemented in the near future.

##### NOTE:

This skill is a _*prototype*_ of how a full-featured help facility
might be implemented in Mycroft.  Comments and suggestions for
improvements are welcome by emailing me at chrison999 (AT) yahoo.ca.
 
