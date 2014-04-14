event = "PRIVMSG"
def call(ircmessage, con):
	nick = ircmessage.prefix.split("!")[0]
	if ircmessage.args[0] == con.nick:
		channel = nick
	else:
		channel = ircmessage.args[0]

	params = ircmessage.args[1].split()
	command = params[0]
	message = " ".join(params[1:])
	if not command == ".echo":
		return

	if len(params) == 1:
		con.privmsg(channel, "help")
		return

	con.privmsg(channel, message)