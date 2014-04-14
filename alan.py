import irc

chanlist = ["#alantest"]

server = "localhost"
port = 6667
nick = "alan"
name = "Alan Turing"
plugdir = "plugins"

con = irc.Server(server, port, nick, name, plugdir)

react = con.react()

for chan in chanlist:
    con.join(chan)

while True:
    msg = con.iqueue.get()
    #print(msg.cmd)
    #con.privmsg("#alantest", msg)