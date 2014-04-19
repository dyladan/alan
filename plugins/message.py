import irc.util
import irc.plugins

import datetime
import collections
import os.path
import pickle
import lockfile


class Plug(irc.plugins.PluginTemplate):
    """Keep messages for later"""
    def __init__(self):
        super(Plug, self).__init__()
        self.name = "message"
        self.helptext = "Saves a message for a user to receive later - usage: .message nick message"
        self.messages = dict()
        self.file = "messages.pickle"
        self.lock = lockfile.FileLock(self.file)
        if os.path.isfile(self.file):
            with open(self.file, "rb") as f:
                self.messages = pickle.load(f)


    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if nick in self.messages:
            for msg in self.messages[nick]:
                con.privmsg(channel, msg)

            del(self.messages[nick])
            self.lock.acquire()
            with open(self.file, "wb") as f:
                pickle.dump(self.messages, f)
            self.lock.release()

            return

        if not params[0] == ".message":
            return

        if not len(params) > 2:
            return

        message = " ".join(params[2:])

        time = str(datetime.datetime.now())[:-7]

        msg = "%s, at %s EST %s said: %s" % (params[1], time, nick, message)

        try:
            self.messages[params[1]].append(msg)
        except:
            self.messages[params[1]] = [msg]

        print(self.messages)

        self.lock.acquire()
        with open(self.file, "wb") as f:
            pickle.dump(self.messages, f)
        self.lock.release()
        con.privmsg(channel, "%s: I'll tell him" % nick)
