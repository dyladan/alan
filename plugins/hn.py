import irc.util
import irc.plugins
import requests
import xmltodict

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "hn"
        self.helptext = "grabs first entry of hacker news | .hn [[num]|[list [num]]]"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        num = 0
        r = requests.get("https://news.ycombinator.com/rss").text
        doc = xmltodict.parse(r)
        stories = doc['rss']['channel']['item']
        if len(params) > 1:
            try:
                num = int(float(params[1]))
                story = stories[num]
                title = story['title']
                link = story['link']
                response = "%s | %s" % (title, link)
                con.privmsg(channel, response)
            except:
                if params[1] == "list":
                    num = 5
                    try:
                        num = int(params[2])
                    except:
                        num = 5
                    num = min(num, 29)
                    for idx, story in enumerate(stories[0:num]):
                        title = story['title']
                        link = story['link']
                        response = "%s | %s | %s" % (idx, title, link)
                        con.privmsg(nick, response)

