os: mac
-
#SHUTDOWNS, RESTARTS, AND ALL THAT JAZZ
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

#FOLDER AND FILE MODIFICATIONS
save (it | that): key(cmd-s)
rename (it | that): user.menu_select('File|Rename')
move (it | that): key(alt-cmd-v)
delete (it | that): key(cmd-delete)
new folder: key(shift-cmd-n)

#FINDER NAVIGATION
help menu: key(cmd-shift-?)
get info: key(cmd-i)
folder view: key(cmd-1)
listview: key(cmd-2)
column view: key(cmd-3)
preview: key(shift-cmd-p)
open sub folders: key(opt-right)
close sub folders: key(opt-left)
cleanup by date: user.menu_select('View|Clean Up By|Date Modified')
cleanup by name: user.menu_select('View|Clean Up By|Name')

go recents: key(shift-cmd-f)
go documents: key(shift-cmd-o)
go desktop: key(shift-cmd-d)
go downloads: key(alt-cmd-l)
go home: key(shift-cmd-h)
go computer: key(shift-cmd-c)
go icloud: key(shift-cmd-i)
go applications: key(shift-cmd-a)
open it: key(cmd-down)
search finder: key(cmd-f)
open with other: 
	user.menu_select('File|Open With|Other…')
	sleep(200ms)
	key(cmd-f)

#FINDER SORTING
sort by date created: user.menu_select('View|Sort Groups By|Date Created')
sort by name: key(ctrl-cmd-1)
sort by kind: key(ctrl-cmd-2)
sort by date last open: key(ctrl-cmd-3)
sort by date added: key(ctrl-cmd-4)
sort by date modified: key(ctrl-cmd-5)
sort by size: key(ctrl-cmd-6)
sort by tags: key(ctrl-cmd-7)