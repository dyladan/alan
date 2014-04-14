event = "NOTICE"
def call(msg, con):
	prefix = msg.prefix.split("!")
	if len(prefix) > 1 and prefix[0] != 'Global':
		nick = prefix[0]
		con.notice(nick, msg)
