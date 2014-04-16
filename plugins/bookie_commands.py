from time import sleep
import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Plugin to aggregate bookie specific things"""
    def __init__(self):
        super(Plug, self).__init__()
        self.helptext = "Bookie plugins - .bhelp for commands"
        self.name = "bookie"
        self.responses = {
        ".logs": "http://logs.bmark.us",
        ".bugs": "https://github.com/bookieio/Bookie/issues",
        ".newbug": "https://github.com/bookieio/Bookie/issues/new",
        ".gh": "https://github.com/bookieio/Bookie",
        ".ot": "Please stay on topic"
        }
        self.help = {
        "logs": "bookie logs",
        "bugs": "github bugs",
        "newbug": "new github bug",
        "gh": "link to github",
        "ot": "offtopic prompt"
        }

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        if params[0] == ".bhelp":
            if len(params) == 1:
                con.privmsg(channel, " | ".join(list(self.help.keys())))
                return
            elif params[1] in self.help:
                con.privmsg(channel, self.help[params[1]])
                return

        if params[0] in self.responses:
            con.privmsg(channel, self.responses[params[0]])