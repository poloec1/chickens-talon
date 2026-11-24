os: mac
app: claude
mode: sleep
-
# Ends Claude dictation, wakes Talon, and removes the typed "stop listening."
stop listening:
	key(cmd-d)
	speech.enable()
	sleep(600ms)
	key(backspace:16)
