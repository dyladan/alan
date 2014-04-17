import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = None
        self.helptext = None
        self.event = "PRIVMSG"
        self.thread = True
        self.private = False
        self.name = None
        self.protected = False

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        pass