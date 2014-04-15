"""Simple plugin management system"""
import os
import imp
import threading


class PluginManager(object):
    """Plugin management object"""
    def __init__(self, plugin_directory, con, cmdchar="."):
        self.con = con
        self.plugs = self.load_plugins(plugin_directory)
        self.cmdchar = cmdchar

    def load_plugins(self, plugin_directory):
        """Returns a list of plugin files"""
        plugins = []

        possible_plugins = os.listdir(plugin_directory)
        print("Possible Plugins:", possible_plugins)

        for plug in possible_plugins:
            try:
                location = os.path.join(plugin_directory, plug)
                if os.path.isdir(location) or not location[-3:] == ".py":
                    continue
                info = imp.find_module(location[:-3])
                mod = imp.load_module(plug, *info)
                plugin = mod.Plug()
                if plugin.event == "CRON":
                    thread = threading.Thread(target=plugin.cron, args=(self.con,))
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
        for plug in self.plugs:
            if arg.cmd == plug.event:
                if self.checkcmd(arg, plug):
                    if plug.thread:
                        thread = threading.Thread(target=plug.call, args=(arg, self.con))
                        thread.start()
                    else:
                        plug.call(arg, self.con)

    def checkcmd(self, msg, plug):
        params = msg.args[1].split()
        if plug.command == "ALL":
            return True
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
            elif plug.command != "ALL":
                commands.append(plug.command)

        return " | ".join(sorted(commands))

    def help(self, plugin):
        for plug in self.plugs:
            if plug.name == plugin:
                return plug.helptext or "No help found"
            if plug.helptext and plug.command == plugin:
                return plug.helptext
        return "No help found for that plugin"


class PluginTemplate(object):
    """Template for plugins"""
    def __init__(self):
        self.command = "ALL"
        self.helptext = None
        self.event = "PRIVMSG"
        self.thread = True
        self.private = False
        self.name = None

    def call(self, msg, con):
        pass



