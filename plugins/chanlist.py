import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    """List all connected channels"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "chanlist"
        self.helptext = "Prints all connected channels"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        con.privmsg(channel, "Current channels: %s" % " ".join(con.channels))
