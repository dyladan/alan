import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "admins"
        self.private = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        admins = con.plugin_mgr.admins

        if admins:
            con.privmsg(channel, "Current admins: %s" % " ".join(admins))
        else:
            con.privmsg(channel, "No currently authorized admins")