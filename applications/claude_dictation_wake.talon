os: mac
app: claude
mode: sleep
-
# Ends Claude dictation, wakes Talon, and removes the typed "dictation done."
dictation done:
	key(cmd-d)
	speech.enable()
	sleep(600ms)
	key(backspace:16)
