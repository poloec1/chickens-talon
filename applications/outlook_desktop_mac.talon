app: Microsoft Outlook
-
#CALENDAR
calendar: key(cmd-2)
new event: user.menu_select('File|New|Event')


#EMAIL
email: key(cmd-1)
next mail: key(down)
last mail: key(up)
unread:
	key(shift-cmd-o)
	sleep(200ms)
	key(down)
mark unread: key(shift-cmd-t)  
reply: key(cmd-r)
react: key(ctrl-cmd-r)
reply all: key(shift-cmd-r)
forward: key(ctrl-cmd-j)
send it: key(cmd-enter)