app: jetbrains
-

#DATABASE
modify view: key(cmd-f6)
query console: key(shift-cmd-l)
generates script: key(alt-cmd-g)
rename: key(shift-f6)
show diagrams: key(alt-shift-cmd-u)
run file: key(ctrl-shift-r)
run it: key(ctrl-r)
debug file: key(ctrl-shift-d)
debug it: key(ctrl-d)
quit it: key(cmd-f2)
ask drunk einstein:
	key(shift-ctrl-i)
target file:
	key(alt-f1)
	sleep(100ms)
	key(1)

#NAVIGATION
go settings:
	key(cmd-,)
	sleep(150ms)
	key(shift-tab)
toggle chat: key(ctrl-shift-c)
toggle database: key(ctrl-alt-cmd-d)
collapse all: key(cmd--)

#FILE COMPARISONS
compare with: key(cmd-d)
next difference: key(f7)
previous difference: key(shift-f7)

#SQL
query all:
	insert('SELECT *')
	key(enter)
	sleep(100ms)
	insert('FROM ')
query where:
	insert('WHERE ')