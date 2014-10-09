import irc.util
import irc.plugins
import time
import xmltodict
import requests

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.event = "CRON"
        self.seen = dict()
        self.secchan = "#security-announce"

    def cron(self, con, start):
        stories = get_all()
        for story in stories:
            self.seen[story['link']] = story['title']

        print(self.seen)
        while True:
            with open('.cron.running', 'r') as f:
                if not f.read() == start:
                    return
            stories = get_all()
            for story in stories:
                if not story['link'] in self.seen:
                    con.privmsg(self.secchan, "%s %s" % (story['link'], story['title']))
                    self.seen[story['link']] = story['title']
            time.sleep(60)
            print("security.py running")

def get_recent():
    stories = get_all()
    story = stories[0]
    return(story)

def get_all():
    r = requests.get("http://www.ubuntu.com/usn/rss.xml").text
    doc = xmltodict.parse(r)
    stories = doc['rss']['channel']['item']
    return(stories)

