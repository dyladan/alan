import time
import irc.util
import irc.plugins
from datetime import datetime


class Plug(irc.plugins.PluginTemplate):
	"""Reloads plugins"""
	def __init__(self):
		super(Plug, self).__init__()
		self.command = "reload"

	def call(self, msg, con):
		nick, channel, params = irc.util.parseprivmsg(msg, con.nick)
		start = datetime.utcnow()
		con.ldplugins(con.plugdir)
		elapsed = datetime.utcnow() - start
		con.privmsg(channel, "reloaded plugins in %s seconds" % elapsed.total_seconds())
		