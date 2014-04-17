import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "part"
        self.protected = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        
        if len(params) == 1:
            con.part(channel)
            return

        con.part(params[1])
