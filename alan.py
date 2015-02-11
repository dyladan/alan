#!bin/python3
import irc

chanlist = ["#geekboy"]

server = "localhost"
port = 6667
nick = "dickbot"
name = "Alan Turing"
plugdir = "gb_plugins"
password = ""

con = irc.Server(server, port, nick, name, plugdir, password)

react = con.react()

for chan in chanlist:
    con.join(chan)

while True:
    try:
        msg = con.iqueue.get()
    except KeyboardInterrupt:
        con.quit("KeyboardInterrupt")

