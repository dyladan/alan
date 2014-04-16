from urllib.request import urlopen

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

        code = urlopen(url).getcode()

        con.privmsg(channel, "%s returns a response code of %s" % (url, code))

