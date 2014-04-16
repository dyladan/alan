import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "source"
        self.helptext = "links to current source code"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        
        con.privmsg(channel, "https://github.com/dyladan/alan")
