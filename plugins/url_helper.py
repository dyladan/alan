import re
import irc.util
import irc.plugins
import urllib.parse
import requests
from lxml import html
import json

class Plug(irc.plugins.PluginTemplate):
    """Shorten any urls"""
    def __init__(self):
        super(Plug, self).__init__()
        self.name = "url helper"
        self.helptext = "scrapes for full URLs - prints title and shortlink to channel"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        if len(params) > 1 and params[0] == ".read":
            return

        if nick == "bookie_sentry":
            return

        message = " ".join(params)

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)

        for url in urls:
            if "bmark.us" in url:
                continue
            if "bookie.io" in url:
                continue

            print(url)
            page = requests.get(url)
            if 'content-type' in page.headers:
                content_type = page.headers['content-type']
                print("%s link found" % content_type)
            else:
                content_type = "Unknown content type"

            title = content_type

            if "html" in content_type:
                content = page.text
                tree = html.fromstring(page.text)
                title_node = tree.xpath('//title/text()')
                print(title_node)
                if title_node:
                    title = "%s" % " ".join(title_node[0].split())
            else:
                content = None

            request = "https://www.googleapis.com/urlshortener/v1/url"

            payload = {"longUrl": url}
            headers = {'content-type': 'application/json'}

            print("%s %s" %(request, payload))
            googl = requests.post(request, data=json.dumps(payload), headers=headers).json()

            response = googl

            print(response)

            if "id" in googl:
                shorturl = googl["id"]
                output = "%s - %s" % (shorturl, title)
            else:
                shorturl = url
                output = "%s" % title

            con.privmsg(channel, output)

            if channel == "#bookie":
                return

            apikey = ""
            with open("bookiebot.apikey") as keyfile:
                apikey = keyfile.read().strip()

            api = "https://bookie.io/api/v1/bookiebot/bmark?api_key=%s" % apikey

            payload = {
                'url': url,
                'description': title,
                'tags': nick
            }

            if False and content:
                payload['content'] = content

            print(payload)
            response = requests.post(api, data=payload, verify=False)

            print(response.text)

