import os
import re

import irc.plugins


class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "memory"
        self.helptext = "returns memory usage of bot"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        con.privmsg(channel, memory())


def memory():
    """.memory - Displays the bot's current memory usage."""
    if os.name == "posix":
        # get process info
        sfile = open('/proc/self/status')
        status_file = sfile.read()
        s = dict(re.findall(r'^(\w+):\s*(.*)\s*$', status_file, re.M))
        # get the data we need and process it
        data = s['VmRSS'], s['VmSize'], s['VmPeak'], s['VmStk'], s['VmData']
        data = [float(i.replace(' kB', '')) for i in data]
        strings = [convert_kilobytes(i) for i in data]
        # prepare the output
        out = "Threads: \x02{}\x02, Real Memory: \x02{}\x02, Allocated Memory: \x02{}\x02, Peak " \
              "Allocated Memory: \x02{}\x02, Stack Size: \x02{}\x02, Heap " \
              "Size: \x02{}\x02".format(s['Threads'], strings[0], strings[1], strings[2],
                                        strings[3], strings[4])
        # return output
        sfile.close()
        return out

    elif os.name == "nt":
        cmd = 'tasklist /FI "PID eq %s" /FO CSV /NH' % os.getpid()
        out = os.popen(cmd).read()
        memory = 0
        for amount in re.findall(r'([,0-9]+) K', out):
            memory += float(amount.replace(',', ''))
        memory = convert_kilobytes(memory)
        return "Memory Usage: \x02{}\x02".format(memory)

    else:
        return "Sorry, this command is not supported on your OS."


def convert_kilobytes(kilobytes):
    if kilobytes >= 1024:
        megabytes = kilobytes / 1024
        size = '%.2f MB' % megabytes
    else:
        size = '%.2f KB' % kilobytes
    return size