import irc.util
import irc.plugins
import subprocess

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "b1ff"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        msg = " ".join(params[1:]).encode()

        p1 = subprocess.Popen("b1ff", stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        output = p1.communicate(input=msg)[0].decode()

        con.privmsg(channel, output)

        pass
