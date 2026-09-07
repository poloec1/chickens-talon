os: mac
app: claude
# fallback if this header doesn't activate: app.bundle: com.anthropic.claudefordesktop
-
# CHAT & FILES
new (chat | conversation): key(cmd-n)
open file: key(cmd-o)

# APP
settings: key(cmd-,)
hide claude: key(cmd-h)

# FIND
find: key(cmd-f)
find next: key(cmd-g)
find previous: key(cmd-shift-g)

# VIEW
reload page: key(cmd-r)
zoom in: key(cmd-+)
zoom out: key(cmd--)
copy url: user.menu_select('View|Copy URL')
full screen: key(fn-f)

# WINDOW
minimize: key(cmd-m)
close window: key(cmd-w)

# PERMISSION PROMPT (tool-trust dialog)
# Stable across both prompt variants: Deny is always 1; Allow once is always cmd-enter.
# "Always allow" has no stable key (it's 2 on the 3-option prompt but absent on the
# 2-option one, where 2 means Allow once), so pick it manually when you want it.
deny: key(1)
(allow once | allow): key(cmd-enter)

# WRITING TOOLS (no shortcut — via menu)
proofread: user.menu_select('Edit|Writing Tools|Proofread')
rewrite: user.menu_select('Edit|Writing Tools|Rewrite')
summarize: user.menu_select('Edit|Writing Tools|Summarize')

# READ ALOUD (presses the read-aloud button on the latest response, via accessibility)
read aloud: user.claude_read_latest()
stop aloud: user.claude_stop_aloud()
read aloud debug: user.claude_read_debug()
read aloud probe: user.claude_read_probe()
