from gi.repository import Gtk


class RecordItem(Gtk.ListBoxRow):
    def __init__(self, filename, time, weight, delete_cb):
        Gtk.ListBoxRow.__init__(self)

        self.filename = filename
        self.delete_cb = delete_cb

        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/record_item.ui")
        self.builder.connect_signals(self)

        filename_lbl = self.builder.get_object("filename_lbl")
        time_lbl = self.builder.get_object("time_lbl")
        weight_lbl = self.builder.get_object("weight_lbl")

        filename_lbl.set_text(filename)
        time_lbl.set_text(time)
        weight_lbl.set_text(weight)

        hbox = self.builder.get_object("record_item")
        self.add(hbox)

    def on_delete_btn_clicked(self, _):
        self.delete_cb(self.filename)

    def on_play_btn_clicked(self, _):
        print("play")

