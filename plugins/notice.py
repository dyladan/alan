import irc.plugins

class Plug(irc.plugins.PluginTemplate):
	"""Replies to notice events"""
	def __init__(self):
		super(Plug, self).__init__()
		self.event = "NOTICE"

	def call(self, msg, con):
		prefix = msg.prefix.split("!")
		if len(prefix) > 1 and prefix[0] != 'Global':
			nick = prefix[0]
			con.notice(nick, msg)
