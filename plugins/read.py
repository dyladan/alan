import irc.util
import irc.plugins
import requests

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "read"
        self.helptext = ".read <url>"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        payload = {'url': params[1]}
        response = requests.post("http://r.bmark.us/api/v1/parse", data=payload).json()
        hash_id = response['data']['hash_id']
        url = "http://r.bmark.us/u/%s" % hash_id
        con.privmsg(channel, url)
