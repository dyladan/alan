import datetime
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
	"""Print system uptime"""
	def __init__(self):
		super(Plug, self).__init__()
		self.command = "uptime"
		self.helptext = "returns uptime of current instance of this bot"

	def call(self, msg, con):
		nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

		runtime = datetime.datetime.utcnow() - con.start

		con.privmsg(channel, str(runtime))
