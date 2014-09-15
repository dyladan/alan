import irc.util
import irc.plugins
from breadability.readable import Article
import requests
import random

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "bread"
        self.helptext = ".bread <url>"
        lower = list(map(chr, range(97, 123)))
        upper = list(map(chr, range(65, 91)))
        nums = list(map(str, range(0,10)))
        self.chars = lower + upper + nums
        self.prefix = "/var/www/read/"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        html = requests.get(params[1]).text
        readable = Article(html, url="http://google.com").readable
        filename = "".join(random.sample(self.chars, 3))
        print(filename)
        with open(self.prefix + filename, "w") as f:
            f.write('<html><body style="width:800px;margin-right:auto;margin-left:auto;"><meta http-equiv="Content-Type" content="text/html;charset=utf-8">')
            f.write(readable)
            f.write('</body></html>')

        con.privmsg(channel, "http://read.dyladan.me/%s" % filename)
