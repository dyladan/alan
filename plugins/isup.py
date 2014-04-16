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

        if self.isup(params[1]):
            message = "Looks up to me"
        else:
            messate = "oh no looks down"

        con.privmsg(channel, message)

    def isup(self, domain):
        request = urlopen('http://www.isup.me/' + domain).read()
        if type(request) != type(''):
            request = request.decode('utf-8')
        return bool("It's just you" in request)