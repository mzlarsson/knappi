
import importlib
import os

PLUGIN_DIR = "plugins"

def load_plugin(path):
    try:
        module_path = (path.replace('/', '.').replace('\\', '.'))[:-3]
        module = importlib.import_module(module_path)
        if hasattr(module, 'get_plugin'):
            plugin = module.get_plugin()
            print("Loaded plugin %s (prio %d)" % (plugin.get_name(), plugin.get_prio()))
            return plugin
        else:
            print("Skipping file %s (no get_plugin func found)" % path)
    except ImportError as err:
        print("Warning: Could not import %s: %s" % (module_path, err))

def load_plugins_from_path(path):
    plugins = []
    for root, dirs, files in os.walk(path, True):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                plugin = load_plugin(os.path.join(root, file))
                if plugin:
                    plugins.append(plugin)
    plugins.sort(key=lambda plugin: plugin.get_prio(), reverse=True)
    return plugins
                
def load_all_plugins():
    return load_plugins_from_path(PLUGIN_DIR)