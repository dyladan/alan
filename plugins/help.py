import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    """Help commands"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "help"
        self.private = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        return

        if len(params) == 1:
            plugs = " | ".join(con.plugin_mgr.listplugins())
            con.privmsg(channel, plugs)
            return

        helptext = con.plugin_mgr.help(" ".join(params[1:]))

        if helptext:
            con.privmsg(channel, helptext)
