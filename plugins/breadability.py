import irc.util
import irc.plugins
from breadability.readable import Article

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "read"
        self.helptext = ".read <url>"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        html = requests.get(params[1]).text
        print(html)
        pass
