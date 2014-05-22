import irc.util
import irc.plugins
import requests

class Plug(irc.plugins.PluginTemplate):
    """Describe your plugin here"""
    def __init__(self):
        super(Plug, self).__init__()
        self.command = "stock"
        self.helptext = ".stock <symbol> - get stock data"

    def call(self, ircmessage, con):
        nick, channel, params = irc.util.parseprivmsg(ircmessage, con.nick)

        if len(params) == 1:
            return

        url = "https://query.yahooapis.com/v1/public/yql"
        q = 'SELECT * FROM yahoo.finance.quotes WHERE symbol="%s" LIMIT 1' % params[1]
        payload = {
            'q': q,
            'format': 'json',
            'env': 'store://datatables.org/alltableswithkeys'
        }

        

        value = requests.get(url, params=payload).json()

        stock = value["query"]["results"]["quote"]

        if float(stock['Change']) < 0:
            stock["Color"] = "5"
        else:
            stock['Color'] = "3"

        msg = "%(Name)s - $%(LastTradePriceOnly)s " \
          "\x03%(Color)s%(Change)s (%(PercentChange)s)\x03 " \
          "H:$%(DaysHigh)s L:$%(DaysLow)s O:$%(Open)s " \
          "Volume:%(Volume)s [%(LastTradeTime)s]" % stock

        con.privmsg(channel, msg)
