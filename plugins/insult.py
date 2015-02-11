import random

import irc.util
import irc.plugins

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "insult"
        self.helptext = "insults people - usage: .insult [nick]"
        self.event = "PRIVMSG"
        self.thread = True
        self.private = False
        self.name = None
        self.protected = False

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if len(params) == 1:
            con.privmsg(channel, self.insult())
        else:
            con.privmsg(channel, self.insult(params[1]))

    def insult(self, name = None):
        one = ['Mouse Humping', 'Lazy', 'Stupid', 'Mother', 'Insecure', 'Spastic', 'Idiotic', 'Disgusting', 'Slimy', 'Slutty', 'Smelly', 'Communist', 'Dicknose', 'Racist', 'Drug Loving', 'Ugly', 'Creepy', 'Shitty', 'Snot Licking', 'Kinky', 'Brother fucking']

        two = ['Douche', 'Ass', 'Turd', 'Shart', 'Rectum', 'Butt', 'Cock', 'Shit', 'Crotch', 'Bitch', 'Turd', 'Prick', 'Slut', 'Fuck', 'Fucking', 'Dick']

        three = ['Pilot', 'Canoe', 'Captain', 'Pirate', 'Hammer', 'Knob', 'Box', 'Jockey', 'Nazi', 'Hillbilly', 'Lawyer', 'Waffle', 'Potato', 'Flower', 'Goblin', 'Dinosaur', 'Infection', 'Blossum', 'Biscuit', 'Clown', 'Socket', 'Monster', 'Hound', 'Dragon', 'Bull', 'Balloon', 'McFaggot', 'Cumjockey']

        v1 = random.choice(one).lower()
        v2 = random.choice(two).lower()
        v3 = random.choice(three).lower()

        if name:
            subject = "%s is a" % name
        else:
            subject = "You"

        insult = "%s %s %s %s." % (subject, v1, v2, v3)

        return insult
