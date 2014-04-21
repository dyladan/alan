import requests

import irc.util
import irc.plugins



class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "np"
        self.helptext = "Check last.fm username now playing - Usage: .np <username>"
        self.api_url = "http://ws.audioscrobbler.com/2.0/"


    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if channel == "#bookie":
            return

        if len(params) == 1:
            return

        user = params[1]

        with open("lastfm.apikey", "r") as keyfile:
            api_key = keyfile.read().strip()

        payload = {'method': 'user.getrecenttracks', 'api_key': api_key, 'user':user, 'limit': '1', 'format': 'json'}
        response = requests.get(self.api_url, params=payload).json()

        print(response)

        if not "track" in response["recenttracks"] or len(response["recenttracks"]["track"]) == 0:
            con.privmsg(channel, "No recent tracks found for %s" % user)

        tracks = response["recenttracks"]["track"]

        if isinstance(tracks, list):  # Partially scrobbled track
            track = tracks[0]
            status = 'current track'
            date = None

        elif isinstance(tracks, dict):  # Last scrobbled track
            track = tracks
            status = 'last track'
            date = track["date"]["#text"]

        else:
            print("Error parsing track listing.")
            return

        title = track["name"]
        album = track["album"]["#text"]
        artist = track["artist"]["#text"]

        ret = "\x02%s\x0F's %s - \x02%s\x0f" % (user, status, title)

        if artist:
            ret += " by \x02%s\x0f" % artist

        if album:
            ret += " on \x02%s\x0f" % album
        if date:
            ret += " [%s]" % date

        con.privmsg(channel, ret)