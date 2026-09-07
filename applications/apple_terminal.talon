app: apple_terminal
-
quit: key(ctrl-c)
enter: key(enter)
suspend: key(ctrl-z)
resume:
    insert("fg")
    key(enter)
clone repo:
	insert("cd ~/Documents/repos")
	key(enter)
	sleep(100ms)
	insert("git clone ")
	sleep(100ms)
	key(cmd-v)
list repositories:
	insert("cd ~/Documents/repos")
	key(enter)
	sleep(100ms)
	insert("ls")
	key(enter)
reveal secrets:
	insert('ls -ld .?*')
	sleep(100ms)
	key(enter)
edit profile:
	insert('nano .zshrc')
	sleep(100ms)
	key(enter)
#VSCODE
code shortcut: 
	insert('code .')
	sleep(150ms)
	key(enter)
	sleep(350ms)
	user.switcher_focus('Code')

#CONTEXTS
get context:
	insert("kubectl config get-contexts")
	key(enter)
context prod:
	insert("kubectl config use-context loyalty-k8s-prod")
context dev:
	insert("kubectl config use-context loyalty-k8s-dev")

#AWS
amazon agent:
	insert('kiro-cli')
	sleep(100ms)
	key(enter)

#FOOT PEDAL
key(ctrl-=): tracking.control_toggle()
key(f19):
    # close zoom if open
    tracking.zoom_cancel()
    mouse_click(0)
    # close the mouse grid if open
    user.grid_close()
    # End any open drags
    # Touch automatically ends left drags so this is for right drags specifically
    user.mouse_drag_end()