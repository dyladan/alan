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

    def cron(self, con, start):
        recent = get_recent()

        while True:
            with open('.cron.running', 'r') as f:
                if not f.read() == start:
                    return
            now = get_recent()
            if not now['link'] == recent['link']:
                #send broadcast
                chanlist = ",".join(con.channels)
                message = "UBUNTU SECURITY ANNOUNCE: %s %s" % (now['title'], now['link'])
                con.privmsg(chanlist, message)
                recent = now
            time.sleep(6)

def get_recent():
    r = requests.get("http://www.ubuntu.com/usn/rss.xml").text
    doc = xmltodict.parse(r)
    story = doc['rss']['channel']['item'][0]
    return(story)

