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

        plugs = set()
        for plug in con.plugin_mgr.plugs:
            plugs.add(plug.command)
            con.privmsg(channel, str(plugs))
            return
