import re, collections, sys
import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "spell"
        self.helptext = "fix the spelling of a word - .spell <word>"
        dict = "big.txt"
        with open(dict) as f:
            self.NWORDS = self.train(self.words(f.read()))
        self.alphabet = 'abcdefghijklmnopqrstuvwxqyz'
        print(len(self.NWORDS))

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        if params[1] == 'DICTSIZE':
            con.privmsg(channel, "%s words, %s bytes" % (len(self.NWORDS), sys.getsizeof(self.NWORDS)))
            return
        out = " ".join([self.correct(x) for x in params[1:]])
        con.privmsg(channel, out)

    def words(self, text): return re.findall('[a-z]+', text.lower())

    def train(self, features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model


    def edits1(self, word):
       splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
       deletes    = [a + b[1:] for a, b in splits if b]
       transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
       replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
       inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
       return set(deletes + transposes + replaces + inserts)

    def known_edits2(self, word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.NWORDS)

    def known(self, words): return set(w for w in words if w in self.NWORDS)

    def correct(self, word):
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or ["unknown: " + word]
        return max(candidates, key=self.NWORDS.get)
