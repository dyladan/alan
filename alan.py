#!bin/python3
import irc

chanlist = ["#alan"]

server = "localhost"
port = 6667
nick = "alan"
name = "Alan Turing"
plugdir = "plugins"
password = "password"

con = irc.Server(server, port, nick, name, plugdir, password)

react = con.react()

for chan in chanlist:
    con.join(chan)

while True:
    try:
        msg = con.iqueue.get()
    except KeyboardInterrupt:
        con.quit("KeyboardInterrupt")

