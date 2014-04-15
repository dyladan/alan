from time import sleep
import hashlib
import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Hashing plugin"""
    def __init__(self):
        super(Plug, self).__init__()
        self.helptext = "Does hashes on arguments"

    def call(self, msg, con):
        nick, channel, params = irc.util.parseprivmsg(msg, con.nick)

        if len(params) == 1:
            return

        if not params[0] in ["sha1", "md5", "sha256", "sha512"]:
            return

        con.privmsg(channel, hash(" ".join(params[1:]), params[0]))


def hash(string, hashtype='sha1'):
    hasher = hashlib.new(hashtype)
    buf = string.encode()
    if len(buf) > 0:
        hasher.update(buf)

    return hasher.hexdigest()