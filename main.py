#!/usr/bin/env python3
import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def main_app():
    from main_window import MainWindow

    # Apply Style
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path("style.css")
    screen = Gdk.Screen.get_default()
    Gtk.StyleContext.add_provider_for_screen(
        screen,
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER,
    )

    MainWindow()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main_app())
