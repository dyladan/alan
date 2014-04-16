import os
import re
import platform

import irc.plugins


class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "system"
        self.helptext = "returns system info"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        con.privmsg(channel, system())


def system():
    """.system - Retrieves information about the host system."""
    hostname = platform.node()
    os = platform.platform()
    python_imp = platform.python_implementation()
    python_ver = platform.python_version()
    architecture = '-'.join(platform.architecture())
    cpu = platform.machine()
    return "Hostname: \x02{}\x02, Operating System: \x02{}\x02, Python " \
           "Version: \x02{} {}\x02, Architecture: \x02{}\x02, CPU: \x02{}" \
           "\x02".format(hostname, os, python_imp,
                         python_ver, architecture, cpu)