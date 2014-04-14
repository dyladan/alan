import irc.util
event = "PRIVMSG"
def call(msg, con):
	nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

	if params[0] == '.chanlist':
		con.privmsg(channel, str(con.channels))