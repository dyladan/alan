import re
import irc.util
import irc.plugins
import urllib.parse
import requests
from lxml import html

class Plug(irc.plugins.PluginTemplate):
    """Shorten any urls"""
    def __init__(self):
        super(Plug, self).__init__()
        self.name = "url shortener"
        self.helptext = "scrapes for full URLs in channel"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        message = " ".join(params)

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)

        for url in urls:
            page = requests.get(url)
            tree = html.fromstring(page.text)
            title = "%s" % " ".join(tree.xpath('//title/text()')[0].split())
            encoded = urllib.parse.quote(url)
            request = "http://is.gd/create.php?format=json&url=%s" % encoded

            isgd = requests.get(request).json()

            response = isgd

            if "shorturl" in isgd:
                shorturl = isgd["shorturl"]
            else:
                shorturl = url

            output = "%s - %s" % (shorturl, title)
            con.privmsg(channel, output)
