import irc.util
import irc.plugins
class Plug(irc.plugins.PluginTemplate):
    """Echo Plugin"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "adminecho"
        self.helptext = "Simply echos your message back to you - usage: .echo <args>"
        self.protected = True

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        command = params[0]
        message = " ".join(params[1:])
        
        if len(params) == 1:
            return
        con.privmsg(channel, message)
