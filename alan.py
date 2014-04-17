#!/usr/bin/python3
import irc

chanlist = ["#alantest", "#asdf"]

server = "localhost"
port = 6667
nick = "slevin"
name = "Alan Turing"
plugdir = "plugins"
password = None

con = irc.Server(server, port, nick, name, plugdir, password)

react = con.react()

for chan in chanlist:
    con.join(chan)

while True:
    msg = con.iqueue.get()
    #print(msg)
    #con.privmsg("#alantest", msg)
