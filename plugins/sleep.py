import irc.util
import irc.plugins

import time
class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "sleep"
        self.helptext = "Simply echos your message back to you - usage: .echo <args>"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if len(params) == 1:
            x = 10
        else:
            x = int(params[1])

        time.sleep(x)

        con.privmsg(channel, "slept %s seconds" % x)
