"""Module for extensible IRC bots"""
import queue
import os
import socket
import threading
from datetime import datetime

import irc.util
import irc.models
import irc.plugins


class Server(object):
    """Core connection class"""
    def __init__(self, server, port, nick, name, plugdir=None, password=None):
        self.iqueue = queue.Queue()
        self.oqueue = queue.Queue()
        self.channels = set()
        self.nick = None
        self.name = None
        self.password = password
        self.plugdir = plugdir
        self.plugin_mgr = None
        self.start = datetime.utcnow()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((server, port))
        self.sock.settimeout(0.5)

        self.setnick(nick)
        self.setuser(name)

        if plugdir:
            self.ldplugins(plugdir)

    def ldplugins(self, plugdir):
        """creates a plugin manager to load plugdir"""
        self.plugin_mgr = irc.plugins.PluginManager(plugdir, self, cmdchar=".", password=self.password)

    def setnick(self, nick):
        """Set IRC nick"""
        self.nick = nick
        self.send(irc.util.buildmsg("NICK", nick))

    def setuser(self, name):
        """Set IRC name"""
        self.name = name
        self.send(irc.util.buildmsg("USER", "%s 0 *" % self.nick, name))

    def join(self, chan):
        """Join an IRC channel"""
        self.channels.add(chan)
        if os.path.exists(chan):
            os.remove(chan)
        self.send(irc.util.buildmsg("JOIN", chan))

    def part(self, chan):
        """PART an IRC channel"""
        self.channels.remove(chan)
        self.send(irc.util.buildmsg("PART", chan))

    def quit(self, reason="ByeBye"):
        self.send(irc.util.buildmsg("QUIT","", reason))

    def privmsg(self, chan, msg):
        """Send a PRIVMSG"""
        tail = None
        if len(msg) > 360:
            tail = msg[360:]
            msg = msg[:360]
        data = irc.util.buildmsg("PRIVMSG", chan, msg)
        self.send(data)
        if tail:
            self.privmsg(chan, tail)

    def notice(self, target, msg):
        """Send a NOTICE"""
        data = irc.util.buildmsg("NOTICE", target, msg)
        self.send(data)

    def send(self, msg):
        """send a message to the out queue"""
        self.oqueue.put(msg)

    def react(self):
        """Begin the react loop in a new thread"""

        def threaded_loop():
            """React loop for reading and writing socket"""
            while True:
                if not self.oqueue.empty():
                    out = self.oqueue.get(False)
                    self.sock.send(out)
                    print(out)

                try:
                    data = self.sock.recv(4096)
                    data = data.decode()
                    lines = data.splitlines()
                    for line in lines:
                        print(line)
                        if line[:4] == "PING":
                            pong_server = line[6:-2]
                            pong = irc.util.buildmsg("PONG", pong_server)
                            self.send(pong)
                            continue


                        parsed_message = irc.util.parsemsg(line)

                        if parsed_message[1] == "ERROR":
                            os._exit(0)

                        prefix = parsed_message[0]
                        cmd = parsed_message[1]
                        args = parsed_message[2]

                        irc_message = irc.models.IRCMessage(prefix, cmd, args)

                        time = datetime.utcnow() - self.start

                        if self.plugin_mgr:
                            self.plugin_mgr.handle(irc_message)

                        self.iqueue.put(irc_message)

                except Exception:
                    pass

        react_thread = threading.Thread(target=threaded_loop)
        react_thread.daemon = True
        react_thread.start()
        return react_thread
