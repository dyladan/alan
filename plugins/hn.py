import irc.util
import irc.plugins
import requests
import xmltodict
import operator

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "hn"
        self.helptext = "grabs an entry of hacker news | .hn [[num]|[list [num]]|[list sort [comments|points] [num]]]"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)
        num = 0

        r = requests.get("http://api.ihackernews.com/page")

        doc = r.json()
        stories = doc["items"]

        #what kind of languange dosen't have a switch statment ughhhh
        if len(params)>3:
            if params[1] == "list" and params[2]=="sort":

                num = 5
                try:
                    num = int(params[4])
                except:
                    num = 5

                try:
                    #if command is "list sort comment" or "list sort c"
                    if params[3] == "comments" or params[3]=="c":
                        stories.sort(key=operator.itemgetter('commentCount'),reverse=True)

                    #if command is "list sort points" or "list sort p"
                    elif params[3] == "points" or params[3]=="p":
                        stories.sort(key=operator.itemgetter('points'),reverse=True)

                    #do you want a catch all?
                    else:
                        stories.sort(key=operator.itemgetter('points'),reverse=True)

                except:
                    stories.sort(key=operator.itemgetter('points'),reverse=True)


                for idx, story in enumerate(stories[0:num]):
                    title = story['title']
                    link = story['url']
                    points = story['points']
                    commentCount = story['commentCount']
                    response = "%s | %s | P:%s | C:%s | %s " % (idx,title,points,commentCount, link)
                    con.privmsg(nick, response)

        elif len(params) > 1:
            try:
                num = int(float(params[1]))
                story = stories[num]
                title = story['title']
                link = story['url']
                points = story['points']
                commentCount = story['commentCount']
                response = "%s | P:%s | C:%s | %s " % (title,points,commentCount, link)
                con.privmsg(channel, response)

            except:
                if params[1] == "list":
                    num = 5
                    try:
                        num = int(params[2])
                    except:
                        num = 5
                    num = min(num, 29)
                    for idx, story in enumerate(stories[0:num]):
                        title = story['title']
                        link = story['url']
                        points = story['points']
                        commentCount = story['commentCount']
                        response = "%s | P:%s | C:%s | %s " % (title,points,commentCount, link)
                        con.privmsg(nick, response)

        if not channel == nick:
          con.privmsg(channel, "check your pm")
