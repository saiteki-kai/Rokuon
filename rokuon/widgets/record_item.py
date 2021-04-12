import os
from gi.repository import Gtk
from rokuon.constants import ui_directory

UI_RECORD_ITEM = os.path.join(ui_directory, "record_item.ui")


class RecordItem(Gtk.ListBoxRow):
    def __init__(self, filename, time, size, delete_cb):
        Gtk.ListBoxRow.__init__(self)

        self.filename = filename
        self.delete_cb = delete_cb

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_RECORD_ITEM)
        self.builder.connect_signals(self)

        filename_lbl = self.builder.get_object("filename_lbl")
        time_lbl = self.builder.get_object("time_lbl")
        size_lbl = self.builder.get_object("size_lbl")

        filename_lbl.set_text(filename)
        time_lbl.set_text(time)
        size_lbl.set_text(size)

        hbox = self.builder.get_object("record_item")
        self.add(hbox)

    def on_delete_btn_clicked(self, _):
        self.delete_cb(self.filename)

    def on_play_btn_clicked(self, _):
        print("play")
