Guillotina Content Rules
========================

This is very similar to the great plone.contentrules.

The concepts are the same, a rule consists of:

  - conditions: Conditions to match when deciding to execute this rule. ONLY ONE HAS TO MATCH
  - actions: Actions to perform on the rule


Rules are executed when content is...::

  - added
  - modified
  - removed



API
---

- GET <container>/@content-rules
- POST <container>/@content-rules
- PATCH <container>/@content-rules
- DELETE <container>/@content-rules
