import urllib.parse
import requests

import irc.util
import irc.plugins


class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "bmark"
        self.helptext = "grabs bmark.us bookmarks - Usage: .bmark [username [history]]"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        user = nick
        history = 1

        if len(params) >= 2:
            user = params[1]

        if len(params) >= 3:
            try:
                history = int(params[2])
            except:
                pass

        user = urllib.parse.quote(user)

        r = requests.get('http://bmark.us/api/v1/%s/bmarks?count=100' % user).json()
        url = r['bmarks'][history-1]['url']
        desc = r['bmarks'][history-1]['description']
        con.privmsg(channel, "%s - %s" % (url, desc))
