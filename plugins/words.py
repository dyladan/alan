import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.command = None
        self.helptext = None
        self.event = "PRIVMSG"
        self.thread = True
        self.private = False
        self.name = None
        self.protected = False

        self.words = set()
        self.dictionary = open("/usr/share/dict/words", "r").read()

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if params[0] == ".words":
            con.privmsg(channel, str(self.words))

        for word in params:
            if word in self.dictionary:
                self.words.add(word)