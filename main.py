#!/usr/bin/env python3
import sys
import gi

# pylint: disable=wrong-import-position
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio
from main_window import MainWindow


class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        self.window = None

    def do_activate(self):
        self.load_css()

        if not self.window:
            self.window = MainWindow(application=self)

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

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def load_css(self):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path("style.css")
        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

    def on_preferences(self, _, __):
        print("on_preferences")

    def on_open_folder(self, _, __):
        print("on_open_folder")

    def on_about(self, _, __):
        print("on_about")
        # about_dialog = Gtk.AboutDialog(modal=True)
        # about_dialog.present()


if __name__ == "__main__":
    app = App()
    sys.exit(app.run(sys.argv))
