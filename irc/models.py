"""Contains models for use with sqlalechemy in irc module"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, DateTime
import datetime

BASE = declarative_base()


class IRCMessage(object):
    """Class for IRC commands"""

    def __init__(self, prefix, command, args):

        self.prefix = prefix
        self.cmd = command
        self.args = args

    def __repr__(self):
        return "<IRC(prefix='%s', cmd='%s', args='%s')>" % (
            self.prefix, self.cmd, self.args)


class Privmsg(BASE):
    """Model to store PRIVMSG events"""
    __tablename__ = 'privmsgs'

    __init__ = BASE.__init__

    id = Column(Integer, Sequence('privmsg_id_seq'), primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    channel = Column(String(50))
    nick = Column(String(16))
    message = Column(String(512))

    def __repr__(self):
        return "<Privmsg(channel='%s', nick='%s', message='%s')>" % (
            self.channel, self.nick, self.message)
