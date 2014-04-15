import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    """Help commands"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "help"
        private = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if len(params) == 1:
            plugs = " | ".join(con.plugin_mgr.listplugins())
            con.privmsg(channel, plugs)
            return

        con.privmsg(channel, con.plugin_mgr.help(params[1]))
