import datetime
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
	if not command == ".uptime":
		return

	runtime = datetime.datetime.utcnow() - con.start



	con.privmsg(channel, str(runtime))
