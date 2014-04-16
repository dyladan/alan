import irc.util
import irc.plugins

import datetime
import collections
import os.path
import pickle


class Plug(irc.plugins.PluginTemplate):
    """Keep messages for later"""
    def __init__(self):
        super(Plug, self).__init__()
        self.name = "message"
        self.helptext = "Saves a message for a user to receive later - usage: .message nick message"
        self.messages = dict()
        if os.path.isfile("messages"):
            with open("messages", "rb") as f:
                self.messages = pickle.load(f)


    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if nick in self.messages:
            print(nick, "in messages")
            for msg in self.messages[nick]:
                con.privmsg(channel, msg)

            del(self.messages[nick])
            with open("messages", "wb") as f:
                pickle.dump(self.messages, f)

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

        with open("messages", "wb") as f:
            pickle.dump(self.messages, f)
    
        con.privmsg(channel, "%s: I'll tell him" % nick)
