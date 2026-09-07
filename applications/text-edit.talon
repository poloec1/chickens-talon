app: TextEdit
-

#TALON COMMANDS
first insert:
	insert(': insert(\'\')')
	key(left)
	key(left)
insert: 
	insert('insert(\'\')')
	key(left)
	key(left)
first keypress:
	insert(': key()')
	key(left)
keypress:
	insert('key()')
	key(left)
first menu select:
	insert(': user.menu_select(\'\')')
	key(left)
	key(left)
menu select:
	insert('user.menu_select(\'\')')
	key(left)
	key(left)
sleep <number>:
	insert('sleep(')
	insert(number)
	insert('ms)')
mouse move:
	insert('mouse_move()')
	key(left)
clicky:
	insert('mouse_click(0)')
right clicky:
	insert('mouse_click(1)')
mouse hold:
	insert('mouse_hold(0)')
mouse hold right:
	insert('mouse_hold(1)')
mouse release:
	insert('mouse_release(0)')
mouse release right:
	insert('mouse_release(1)')
close app:
	insert('app.window_close()')
focus app:
	insert('user.switcher_focus()')
	sleep(100ms)
	key(left)