#!bin/python3
import irc

chanlist = ["#geekboy", "#security-announce"]

server = "localhost"
port = 9876
nick = "dickbot"
name = "Alan Turing"
plugdir = "gb_plugins"
password = "fsmor;06"

con = irc.Server(server, port, nick, name, plugdir, password)

react = con.react()

for chan in chanlist:
    con.join(chan)

while True:
    try:
        msg = con.iqueue.get()
    except KeyboardInterrupt:
        con.quit("KeyboardInterrupt")

