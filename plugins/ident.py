import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    """Identify with NickServ"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "ident"
        private = True

    def call(self, ircmessage, con):
            nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

            if len(params) == 1:
                    return
            con.privmsg("NickServ", "IDENTIFY %s" % params[1])
