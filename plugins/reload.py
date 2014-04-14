import time
import irc.util
from datetime import datetime

event = "PRIVMSG"
def call(msg, con):
	nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

	if params[0] == ".reload":
		print('reloading')
		start = datetime.utcnow()
		con.ldplugins(con.plugdir)
		elapsed = datetime.utcnow() - start
		con.privmsg(channel, "reloaded plugins in %s seconds" % elapsed.total_seconds())
	return
