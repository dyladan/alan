import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "join"
        self.private = True
        self.protected = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if len(params) == 1:
            return

        con.join(params[1])
