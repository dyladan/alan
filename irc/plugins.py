"""Simple plugin management system"""
import os
import imp
import threading
import time


class PluginManager(object):
    """Plugin management object"""
    def __init__(self, plugin_directory, con, cmdchar=".", password=None):
        self.con = con
        self.plugs = self.load_plugins(plugin_directory)
        self.cmdchar = cmdchar
        self.admins = set()
        self.password = password

    def load_plugins(self, plugin_directory):
        """Returns a list of plugin files"""
        plugins = []
        t = str(time.time())
        with open(".cron.running", 'w') as f:
            f.write(t)

        possible_plugins = os.listdir(plugin_directory)
        print("Possible Plugins:", possible_plugins)

        for plug in possible_plugins:
            try:
                location = os.path.join(plugin_directory, plug)
                if os.path.isdir(location):
                    print("Found dir %s" % location)
                    continue
                if not location[-3:] == ".py":
                    print("Not a python file %s" % location)
                    continue
                if location.split("/")[-1][0] == "_":
                    print("Ignored %s" % location)
                    continue
                info = imp.find_module(location[:-3])
                mod = imp.load_module(plug, *info)
                plugin = mod.Plug()
                if plugin.event == "CRON":
                    thread = threading.Thread(target=plugin.cron, args=(self.con,t))
                    thread.daemon = True
                    thread.start()
                    continue
                plugins.append(plugin)
            except Exception as ex:
                print(ex)

        print(plugins)
        return plugins

    def handle(self, arg):
        """runs irc msg through plugin manager"""
        if arg.cmd == "PRIVMSG":
            params = arg.args[1].split()
            nick = arg.prefix.split("!")[0]
            if params[0] == self.cmdchar + "auth" and len(params) > 1:
                print("auth requested by %s with password %s" % (nick, params[1]))
                if params[1] == self.password:
                    self.admins.add(nick)
                    self.con.privmsg(nick, "authed")
                    print("current admins: %s" % self.admins)
                    return
        for plug in self.plugs:
            if arg.cmd == plug.event:
                if self.checkcmd(arg, plug):
                    if plug.thread:
                        thread = threading.Thread(target=plug.call, args=(arg, self.con))
                        thread.start()
                    else:
                        plug.call(arg, self.con)


    def checkcmd(self, msg, plug):
        if not plug.command:
            return True

        params = msg.args[1].split()
        nick = msg.prefix.split("!")[0]


        if plug.protected and not nick in self.admins:
            return

        if params[0] == self.cmdchar + plug.command:
            return True
        else:
            return False

    def listplugins(self):
        commands = []
        for plug in self.plugs:
            if plug.private:
                continue
            if plug.name:
                commands.append(plug.name)
            elif plug.command:
                commands.append(plug.command)

        return sorted(commands)

    def help(self, plugin):
        for plug in self.plugs:
            if plug.name == plugin:
                return plug.helptext or None
            if plug.helptext and plug.command == plugin:
                return plug.helptext
        return None


class PluginTemplate(object):
    """Template for plugins"""
    def __init__(self):
        self.command = None
        self.helptext = None
        self.event = "PRIVMSG"
        self.thread = True
        self.private = False
        self.name = None
        self.protected = False

    def call(self, msg, con):
        pass



