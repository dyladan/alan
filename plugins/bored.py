import irc.util
import irc.plugins
import re
import random

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        msg = " ".join(params).lower()
        print(msg)
        if not re.match(r"^i\'m bored", msg):
            return

        with open("bored") as f:
            lines = f.readlines()
            line = random.choice(lines)

            con.privmsg(channel, line)
        pass