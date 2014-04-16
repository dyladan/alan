import datetime
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Print system uptime"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "sysuptime"
        self.helptext = "returns uptime of system"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        con.privmsg(channel, self.sysuptime())


    def sysuptime(self):
        """.sysuptime - Shows the system's uptime."""
        uptime_string = ""
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
        return "Uptime: \x02{}\x02".format(uptime_string[:-7])



        con.privmsg(channel, str(runtime))
