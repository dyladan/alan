import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "broadcast"
        self.helptext = None
        self.event = "PRIVMSG"
        self.thread = True
        self.private = True
        self.name = None
        self.protected = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        chanlist = ",".join(con.channels)

        message = "BROADCAST FROM ADMINISTRATOR: %s" % " ".join(params[1:])

        con.privmsg(chanlist, message)

        pass