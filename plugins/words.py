import os.path
import pickle
import lockfile

import irc.util
import irc.plugins


class Plug(irc.plugins.PluginTemplate):
    def __init__(self):
        super(Plug, self).__init__()
        self.words = dict()
        self.pickle = 'words.pickle'
        self.lock = lockfile.FileLock(self.pickle)
        if os.path.isfile(self.pickle):
            self.lock.acquire()
            with open(self.pickle, "rb") as f:
                self.words = pickle.load(f)
            self.lock.release()

        self.dictionary = open("/usr/share/dict/words", "r").read().lower()

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if params[0] == ".words":
            con.privmsg(channel, str(self.words))
            return

        for word in params:
            if word.lower() in self.dictionary:
                if word in self.words:
                    self.words[word] += 1
                else:
                    self.words[word] = 1

        print("locking")
        self.lock.acquire()
        print("locked")
        with open(self.pickle, "wb") as f:
            pickle.dump(self.words, f)
            print("dumped")
        self.lock.release()
        print("released")
