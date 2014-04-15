import time
import irc.util
import irc.plugins
from datetime import datetime


class Plug(irc.plugins.PluginTemplate):
    """Reloads plugins"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "reload"
        self.helptext = "reloads plugins"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)
        start = datetime.utcnow()
        con.ldplugins(con.plugdir)
        elapsed = datetime.utcnow() - start
        count = len(con.plugin_mgr.listplugins())
        con.privmsg(channel, "reloaded %s plugins in %s seconds" % (count, elapsed.total_seconds()))
        