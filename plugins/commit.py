import irc.util
import irc.plugins

import subprocess


class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "shortlog"
        self.helptext = "shows last pulled commit in working dir"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        current_commit = subprocess.check_output(("git", "rev-parse", "HEAD")).strip().decode()
        commit_shortlog = subprocess.check_output(("git", "shortlog", "HEAD~..HEAD"))
        commit_message = commit_shortlog.splitlines()[1].decode().strip()
        con.privmsg(channel, "Current commit is %s %s" % (current_commit, commit_message))
