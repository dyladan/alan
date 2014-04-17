import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    """Identify with NickServ"""
    def __init__(self):
        super(Plug, self).__init__()
        self.event = "NICK"
        self.private = True

    def call(self, ircmessage, con):
        nick = ircmessage.prefix.split("!")[0]
        if con.plugin_mgr.admins:
            if nick in con.plugin_mgr.admins:
                con.plugin_mgr.admins.remove(nick)
            print(con.plugin_mgr.admins)