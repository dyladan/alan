"""Simple plugin management system"""
import os
import imp
import threading

import irc.util


class PluginManager(object):
    """Plugin management object"""
    def __init__(self, plugin_directory, con):
        self.con = con
        self.plugs = self.load_plugins(plugin_directory)

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
                if mod.event and mod.event == "CRON":
                    thread = threading.Thread(target=mod.cron, args=(self.con,))
                    thread.daemon = True
                    thread.start()
                    continue
                plugins.append(mod)
            except Exception as ex:
                print(ex)

        print(plugins)
        return plugins

    def handle(self, arg):
        """runs irc msg through plugin manager"""
        for plug in self.plugs:
            if arg.cmd == plug.event:
                thread = threading.Thread(target=plug.call, args=(arg, self.con))
                thread.start()
