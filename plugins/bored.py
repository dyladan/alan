import irc.util
import irc.plugins
import random

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "bored"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        with open("bored") as f:
            lines = f.readlines()
            line = random.choice(lines)

            if random.choice([True,False]):
                con.privmsg(channel, "Get high and %s" % line.lower())
            else:
                con.privmsg(channel, line)
