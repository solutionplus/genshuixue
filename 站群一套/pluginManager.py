#!/usr/bin/env python
#!coding=utf-8
###########################################################
 # Author        : xiaoyun.yang
 # Email         : yangxiaoyun@baijiahulian.com
 # Last modified : 2016-04-25 15:21
 # Filename      : pluginManager.py
 # Description   : 
###########################################################
import sys
import os
import logging
from iPlugin import Plugin
from imp import find_module,load_module,acquire_lock,release_lock
import os
import sys

logger = logging.getLogger("data_compute")
class PluginManager(object):
    """Base class for plugin managers. Does not implement loadPlugins, so it
    may only be used with a static list of plugins.
    """
    name = "base"

    def __init__(self, plugins=(), config={}):
        self.__plugins = []
        if plugins:
            self.addPlugins(plugins)

    def __iter__(self):
        return iter(self.plugins)

    def addPlugin(self, plug):
        logger.info( 'PluginManager add plugin:%s'%(plug.name))
        self.__plugins.append(plug)

    def addPlugins(self, plugins):
        for plug in plugins:
            self.addPlugin(plug)

    def delPlugin(self, plug):
        if plug in self.__plugins:
            self.__plugins.remove(plug)

    def delPlugins(self, plugins):
        for plug in plugins:
            self.delPlugin(plug)

    def getPlugins(self,name=None):
        plugins = []
	logger.debug('self.__plugins:')
        for plugin in self.__plugins:
	    logger.debug('plugin.name:%s'%(plugin.name))
            if (name is None or plugin.name == name):
                plugins.append(plugin)
        return plugins

    def _loadPlugin(self, plug):       
        loaded = False
	logger.info('******PluginManager  _loadPlugin:')
        for p in self.plugins:
            if p.name == plug.name:
                loaded = True
                break
        if not loaded:
            self.addPlugin(plug)
            logger.info("%s: loaded plugin %s " % (self.name, plug.name))

    def loadPlugins(self):
        pass

    def _get_plugins(self):
        return self.__plugins

    def _set_plugins(self, plugins):
        self.__plugins = []
        self.addPlugins(plugins)

    plugins = property(_get_plugins, _set_plugins, None,
                       """Access the list of plugins managed by
                       this plugin manager""")
    
    
class DirectoryPluginManager(PluginManager):
    """Plugin manager that loads plugins from plugin directories.
    """
    name = "directory"

    def __init__(self, plugins=(), config={}):
        default_directory = os.path.join(os.path.dirname(__file__),"plugins")
        self.directories = config.get("directories", (default_directory,))
        logger.info('========DirectoryPlugManager========')
        PluginManager.__init__(self, plugins, config)

    def loadPlugins(self):
        """Load plugins by iterating files in plugin directories.
        """
        plugins = []
        logger.info('********Directory directories:%s'%(self.directories))
        for dir in self.directories:
            try:
                for f in os.listdir(dir):
                    if f.endswith(".py") and f != "__init__.py":
                        plugins.append((f[:-3], dir))
            except OSError:
                logger.error( "Failed to access: %s" %(dir))
                continue

        fh = None
        mod = None
        logger.info( '********Directory all plugins:')
        for (name, dir) in plugins:
            try:
                acquire_lock()
                fh, filename, desc = find_module(name, [dir])
                logger.info('********Directory fh,filename,desc:%s,%s,%s,%s'%(fh,filename,desc,name))
                old = sys.modules.get(name)
                if old is not None:
                    # make sure we get a fresh copy of anything we are trying
                    # to load from a new path
                    del sys.modules[name]
                mod = load_module(name, fh, filename, desc)
            finally:
                if fh:
                    fh.close()
                release_lock()
            if hasattr(mod, "__all__"):
                logger.info('********Directory mod  __all__:%s'%(mod.__all__))
                attrs = [getattr(mod, x) for x in mod.__all__]
                logger.info('********Directory attrs:%s'%(attrs))
                for plug in attrs:
                    if not issubclass(plug, Plugin):
                        continue
                    self._loadPlugin(plug())
