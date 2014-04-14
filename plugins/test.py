from time import sleep


event = "PRIVMSG"
def call(ircmessage, con):
	sleep(2)
	print("called test", ircmessage.args)