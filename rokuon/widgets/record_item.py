import os
from gi.repository import Gtk
from rokuon.constants import ui_directory, save_directory

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
        size_lbl.set_text(size.rjust(4, '0'))
        # TODO: align better the label
        # IDEA: testo a sinistra con dimensione fissa, il tempo
        # ha sempre la stessa lunghezza, si allinea la size a sinistra ??

        hbox = self.builder.get_object("record_item")
        self.add(hbox)

    def on_delete_btn_clicked(self, _):
        self.delete_cb(self.filename)

    def on_play_btn_clicked(self, _):
        from pydub import AudioSegment
        from pydub.playback import play
        import threading

        filepath = os.path.join(save_directory, self.filename)
        sound = AudioSegment.from_file(filepath, 'mp3')

        # TODO: handle only one play at time
        # TODO: terminate thread when closing the app
        t = threading.Thread(target=play, args=(sound,))
        t.start()
