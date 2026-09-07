os: mac
app: slack
-
(slack | lack) channels: mouse_move(195.0, 427.0)
(slack | lack) (messages | chat): mouse_move(762.0, 276.0)
emoji <user.text>:
	insert(':')
	sleep(50ms)
	insert("{text}")
gif <user.text>:
	insert('/g')
	sleep(100ms)
	key(enter)
	insert('{text}')