# Part of Carburetor project
# Released under GPLv3+ License
# Danial Behzadi<dani.behzi@ubuntu.com>, 2020-2023.

"""
handle ui related stuff
"""

from gi.repository import Gdk, Gio, Gtk

from . import config
from . import handler


builder = Gtk.Builder(scope_object_or_map=handler)
ui_dir = config.s_data_dir + "/ui"


def initialize_builder() -> None:
    """
    connect builder to files and handlers
    """
    resource = Gio.resource_load(config.s_data_dir + "/res.gresource")
    Gio.resources_register(resource)
    prefix = "/io/frama/tractor/carburetor/gtk/"
    builder.add_from_resource(prefix + "main.ui")
    builder.add_from_resource(prefix + "preferences.ui")
    builder.add_from_resource(prefix + "help-overlay.ui")


def get(obj: str):
    """
    get object from ui
    """
    return builder.get_object(obj)


def css() -> None:
    """
    apply css to ui
    """
    css_provider = Gtk.CssProvider()
    prefix = "/io/frama/tractor/carburetor/gtk/"
    css_provider.load_from_resource(prefix + "style.css")
    display = Gdk.Display.get_default()
    Gtk.StyleContext.add_provider_for_display(
        display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
    )
