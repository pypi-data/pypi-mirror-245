Project cmd~ai~
===============

*Another ChatGPT project implemented in a shell command*

README for version `0.0.3`

Installation
------------

It should work with `pip install`, not tested.

Needs `API_KEY` for OpenAI in `~/.openai.token`

Features
--------

-   conversation in terminal with gpt4
-   incremental saving conversation to `conversations.org`
-   *pythonista* mode
-   *sheller* mode (both with a simple system prompt)
-   show spent money
-   save code to `/tmp` and execute with `.e`

Help
----

``` {.example}
.h      help
.q      quit
.e      execute code
.r      reset messages, scripts
.l      show tokens
.m      show models
.l number ... change limit tokens
________________ ROLES _____________
.a   assistent
.t   NO translator
.p   python coder
.s   shell expert
.d   NO dalle
________________ MODEL
.i   NO use dalle
.v   NO use vision
```

### Assistent

Instructed to be brief and clear, non-repetitive

### Pythonista

Be brief, one code block per answer max. Creates a file in /tmp and lets
it run with `.e`

### Sheller

Similar but for bash

### Piper

Works only from commandline, when pipe (stdin) is detected. No memory,
on task/question, asks before runs the code
