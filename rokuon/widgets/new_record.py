import os
import shutil
from time import time
from gi.repository import Gtk
from rokuon.constants import ui_directory, tmp_directory

UI_NEW_RECORD = os.path.join(ui_directory, "new_record.ui")


class NewRecord(Gtk.ListBoxRow):
    def __init__(self, save_cb):
        Gtk.ListBoxRow.__init__(self)

        self.save_cb = save_cb

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_NEW_RECORD)
        self.builder.connect_signals(self)

        ext = "mp3"
        self.entry = self.builder.get_object("filename_entry")
        self.entry.set_text(f"{int(time() * 1000)}.{ext}")

        hbox = self.builder.get_object("record_list_item")
        self.add(hbox)

    def on_save_btn_clicked(self, _):
        filename = self.entry.get_text()
        tmp_file = os.path.join(tmp_directory, "temp.mp3")

        if filename and not filename.isspace() and os.path.exists(tmp_file):
            dest_dir = os.path.join(os.path.expanduser("~"), "Audio")
            shutil.move(tmp_file, f"{dest_dir}/{filename}")
        self.save_cb()
