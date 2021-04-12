import os
import gi

# pylint: disable=wrong-import-position
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio
from rokuon.views.main_window import MainWindow
from rokuon.constants import ui_directory


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        # self.load_css()
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(app=self)
        self.window.show()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction(name="preferences")
        action.connect("activate", self.on_preferences)
        self.add_action(action)

        action = Gio.SimpleAction(name="openfolder")
        action.connect("activate", self.on_open_folder)
        self.add_action(action)

        action = Gio.SimpleAction(name="about")
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction(name="quit")
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def load_css(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(os.path.join(ui_directory, "style.css"))
        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def on_preferences(self, _, __):
        print("on_preferences")

    def on_open_folder(self, _, __):
        print("on_open_folder")

    def on_about(self, _, __):
        print("on_about")
        # about_dialog = Gtk.AboutDialog(modal=True)
        # about_dialog.present()

    def on_quit(self, _, __):
        print("quit")
        self.quit()
