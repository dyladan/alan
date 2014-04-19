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
        self.name = "url helper"
        self.helptext = "scrapes for full URLs - prints title and shortlink to channel"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        message = " ".join(params)

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)

        for url in urls:
            page = requests.get(url)
            if 'content-type' in page.headers:
                content_type = page.headers['content-type']
                print("%s link found" % content_type)
            else:
                content_type = "Unknown content type"

            title = content_type

            if "html" in content_type:
                tree = html.fromstring(page.text)
                title_node = tree.xpath('//title/text()')
                print(title_node)
                if title_node:
                    title = "%s" % " ".join(title_node[0].split())

            encoded = urllib.parse.quote(url)
            request = "http://is.gd/create.php?format=json&url=%s" % encoded

            isgd = requests.get(request).json()

            response = isgd

            if "shorturl" in isgd:
                shorturl = isgd["shorturl"]
                output = "%s - %s" % (shorturl, title)
            else:
                shorturl = url
                output = "%s" % title

            con.privmsg(channel, output)
