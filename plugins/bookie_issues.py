import re
import irc.util
import irc.plugins
import requests
import re

class Plug(irc.plugins.PluginTemplate):
    """Find bookie pull issues"""
    def __init__(self):
        super(Plug, self).__init__()
        self.name = "bookie issue helper"
        self.helptext = "scrapes issues in the form #232"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        if not channel in ["#bookie", "#ubuntu-us-mi", "#asdf"]:
            return

        for arg in params:
            match = re.match(r"#(\d+)$", arg)
            if match:
                issue = github_issue(match.group(1))
                out = " - ".join([issue['state'], issue['title'], issue['html_url']])
                if issue:
                    con.privmsg(channel,out)

def github_issue(issue):
    r = requests.get("https://api.github.com/repos/bookieio/bookie/issues/%s" % issue)
    if r.status_code == 200:
        json = r.json()
        return json
    else:
        return None
