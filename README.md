# Getting started
In order to apply these Workspace Settings in your project, go to the folder where you usually clone your git repositories and copy `.vscode/` there.

## Why bother
Code is read much more often than it is written.
This is intended to improve the readability of code and make it consistent.

> Readability counts.
> 
> &nbsp;   &nbsp;   &nbsp; — PEP 20 - The Zen of Python

> Consistency with this style guide is important. However, know when to be inconsistent. Sometimes style guide recommendations just aren't applicable.
> When in doubt, use your best judgment. Look at other examples and decide what looks best. And don't hesitate to ask!
>
> In particular: do not break backwards compatibility just to comply with this PEP!
> 
> &nbsp;   &nbsp;   &nbsp; — PEP 8 - Style Guide for Python Code

## What's here
```sh
$ tree .vscode/
.vscode/
|-- .gitignore                  # ref for python repos, adjust to suit yourself
|-- esP_script_snippet.conf     # sample .conf file,    just for illustration
|-- esP_script_snippet.py       # sample .py file,      just for illustration
|-- keybindings.json            # at now, just correct tab order
|-- settings.json               # at now, formatting preferences
|-- settings.conf.code-snippets # insert .conf template typing Ctrl+Space
`-- settings.py.code-snippets   # insert .py   template typing Ctrl+Space
```
