from urllib.request import urlopen
from datetime import datetime

import irc.util
import irc.plugins


class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "isup"
        self.helptext = "Checks if server is up or down - usage: .isup <server>"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if len(params) == 1:
            return

        url = params[1]

        if not url[:4] == "http":
            url = "http://" + url

        try:
            start = datetime.utcnow()
            code = urlopen(url).getcode()
            end = datetime.utcnow()

            duration = (end - start).total_seconds()

            con.privmsg(channel, "%s returned a response code of %s in %s seconds" % (url, code, duration))
        except:
            con.privmsg(channel, "%s appears to be down" % url)
