app: kiro
-
tag(): user.tabs
tag(): user.line_commands
tag(): user.find_and_replace
tag(): user.multiple_cursors
tag(): user.command_client

# Panels
panel solution: key(ctrl-alt-l)
panel properties: key(f4)
panel output: key(ctrl-alt-o)
panel class: key(ctrl-shift-c)
panel errors: key(ctrl-\ ctrl-e)
panel design: key(shift-f7)
panel marks: key(ctrl-k ctrl-w)
panel breakpoints: key(ctrl-alt-b)

# Settings
show settings: key(alt-t o)

# Display
fullscreen switch: key(shift-alt-enter)
wrap switch: key(ctrl-e ctrl-w)

# File Commands
file hunt [<user.text>]:
	key(ctrl-shift-t)
	insert(text or "")
file create: key(ctrl-n)
file rename: key(ctrl-[ s f2)
file reveal: key(ctrl-[ s)

# Language Features
hint show: key(ctrl-shift-space)
definition show: key(f12)
definition peek: key(alt-f12)
references find: key(shift-f12)
format that: key(ctrl-k ctrl-d)
format selection: key(ctrl-k ctrl-f)
imports fix: key(ctrl-r ctrl-g)

refactor field: key(ctrl-r ctrl-e)
refactor interface: key(ctrl-r ctrl-i)
refactor method: key(ctrl-r ctrl-m)
refactor reorder parameters: key(ctrl-r ctrl-o)
refactor remove parameters: key(ctrl-r ctrl-v)
refactor that: key(ctrl-r ctrl-r)

#code navigation
(go declaration | follow): key(ctrl-f12)
go back: key(ctrl--)
go forward: key(ctrl-shift--)
go implementation: key(f12)
go recent [<user.text>]:
	key(ctrl-1 ctrl-r)
	sleep(100ms)
	insert(text or "")
go type [<user.text>]:
	key(ctrl-1 ctrl-t)
	sleep(100ms)
	insert(text or "")
go member [<user.text>]:
	key(alt-\)
	sleep(100ms)
	insert(text or "")
go usage: key(shift-f12)

# Bookmarks.
go marks: key(ctrl-k ctrl-w)
toggle mark: key(ctrl-k ctrl-k)
go next mark: key(ctrl-k ctrl-n)
go last mark: key(ctrl-k ctrl-p)

# Folding
fold toggle: key(ctrl-m ctrl-m)
fold toggle all: key(ctrl-m ctrl-l)
fold definitions: key(ctrl-m ctrl-o)

#Debugging
break point: key(f9)
step over: key(f10)
debug step into: key(f11)
debug step out [of]: key(f10)
debug start: key(f5)
debug stopper: key(shift-f5)
debug continue: key(f5)

# project
open project:
	key(cmd-o)
	sleep(450ms)
	#go to documents
	key(shift-cmd-o)
	sleep(200ms)
	insert("repo")
	sleep(200ms)
	key(cmd-right)

# NAVIGATION
toggle search: key(shift-cmd-f)

# Navigating Explorer aka how you move around the files
toggle project: key(shift-cmd-e)
toggle commit: key(ctrl-shift-g)
collapse folders: key(ctrl-cmd-c)
toggle right sidebar: key(alt-cmd-b)
toggle left sidebar: key(cmd-b)

toggle chat: key(ctrl-cmd-i)
toggle scope: key(ctrl-shift-cmd-c)
toggle output: key(shift-cmd-u)
toggle panel: key(cmd-j)
toggle terminal: key(ctrl-cmd-t)
new terminal: key(ctrl-shift-`)
focus panel: key(ctrl-cmd-j)
split right: key(cmd-\)
close all saved:
	key(cmd-k)
	sleep(200ms)
	key(u)
close all:
	key(cmd-k)
	sleep(200ms)
	key(w)

# drunk einstein help aka autocomplete/copilot
quick fix: key(cmd-.)
inline chat: key(cmd-i)
new chat: key(cmd-n)

# find and replace
replace it: key(alt-cmd-f)

#CURSORLESS
hints toggle: key(ctrl-alt-cmd-t)

#KIRO
ghost ask: key(cmd-l)
ghost goodbye: key(cmd-w)
ghost trust: key(shift-cmd-enter)
ghost run: key(cmd-enter)
#ghost log in: fixed-position login button, no shortcut/menu — hardcoded coords accepted per house style
ghost log in:
	mouse_move(956.42578125, 639.59375)
	sleep(150ms)
	mouse_click(0)
ghost new:
	key(shift-cmd-l)
ghost focus:
	key(cmd-l)
ghost (clothes | close):
	key(cmd-w)
