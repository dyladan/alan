import irc.util
import irc.plugins

import requests
import urllib.parse


class Plug(irc.plugins.PluginTemplate):
    """Plugin to aggregate bookie specific things"""
    def __init__(self):
        super(Plug, self).__init__()
        self.helptext = "Bookie plugins - .b for commands"
        self.command = "b"
        self.responses = {
        "logs": "http://logs.bmark.us",
        "bugs": "https://github.com/bookieio/Bookie/issues",
        "newbug": "https://github.com/bookieio/Bookie/issues/new",
        "gh": "https://github.com/bookieio/Bookie",
        "ot": "Please stay on topic"
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

        if len(params) == 1:
            con.privmsg(channel, " | ".join(list(self.help.keys())))
            return
        
        if params[1] in self.help:
            con.privmsg(channel, self.responses[params[1]])
            return
