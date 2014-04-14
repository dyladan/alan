"""Contains utility functions for irc module"""


def parsemsg(message):
    """Breaks a message from an IRC server into its
    prefix, command, and arguments.
    """
    prefix = ''
    trailing = []
    if not message:
        raise Exception("Empty line.")
    if message[0] == ':':
        prefix, message = message[1:].split(' ', 1)
    if message.find(' :') != -1:
        message, trailing = message.split(' :', 1)
        args = message.split()
        args.append(trailing)
    else:
        args = message.split()
    command = args.pop(0)
    return prefix, command, args


def buildmsg(command, arg=None, payload=None):
    """Given parameters builds a message to be sent to IRC server"""
    command = command.upper()

    if arg and payload:
        msg = "%s %s :%s\r\n" % (command, arg, payload)
    elif arg:
        msg = "%s %s\r\n" % (command, arg)
    elif payload:
        msg = "%s :%s\r\n" % (command, payload)
    else:
        raise Exception("IRCBadMessage")

    return msg.encode()
