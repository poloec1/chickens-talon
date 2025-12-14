os: mac
-
#Force quits all running applications
app bedtime: 
	key(alt-cmd-escape)
	sleep(100ms)
	key(cmd-a)
	sleep(100ms)
	key(enter)
	sleep(100ms)
	key(enter)
force quit:
	key(alt-cmd-escape)
quit it:
	key(enter)
	sleep(300ms)
	key(enter)
	sleep(400ms)
	key(alt-cmd-escape)
	sleep(300ms)
	app.window_close()
lock computer screen:
	key(ctrl-cmd-q)
restart computer:
	user.menu_select('Apple|Restart…')
	sleep(100ms)
	key(enter)
shutdown computer:
	user.menu_select('Apple|Shut Down…')
	sleep(100ms)
	key(enter)
save that: key(cmd-s)
rename it: user.menu_select('File|Rename')

#Navigation
help menu: key(cmd-shift-?)
folder view: key(cmd-1)
listview: key(cmd-2)
column view: key(cmd-3)
preview: key(shift-cmd-p)
open sub folders: key(opt-right)
close sub folders: key(opt-left)
move it: key(opt-cmd-v)
go recent: key(shift-cmd-f)
go documents: key(shift-cmd-o)
go desktop: key(shift-cmd-d)
go downloads: key(alt-cmd-l)
go home: key(shift-cmd-h)
go computer: key(shift-cmd-c)
go icloud: key(shift-cmd-i)
go applications: key(shift-cmd-a)