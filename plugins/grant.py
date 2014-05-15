import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "grant"
        self.helptext = None
        self.event = "PRIVMSG"
        self.thread = True
        self.private = True
        self.name = None
        self.protected = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if len(params) == 1:
            return

        con.plugin_mgr.admins.add(params[1])
        self.con.privmsg(nick, "authed")
