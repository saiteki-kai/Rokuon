from gi.repository import Gtk
from pulse_recorder import Recorder


class MainWindow:
    def __init__(self, app):
        self.app = app

        self.builder = Gtk.Builder()
        self.builder.add_from_file("main_window.ui")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.window.set_application(self.app)

        # Setup Menu
        self.builder.add_from_file("menubar.ui")
        menu_btn = self.builder.get_object("menu_btn")
        menu = self.builder.get_object("appmenu")
        menu_btn.set_menu_model(menu)

        self.selected_index = None
        self.recorder = Recorder()

        self.record_list = self.builder.get_object("record_list")
        self.source_store = self.builder.get_object("source_store")
        self.source_combo = self.builder.get_object("source_combo")

        self.source_combo.set_active(0)
        self.populate_sources()

        self.change_record_state()
        self.add_record()

    def show(self):
        self.window.show_all()

    def destroy(self, _):
        self.recorder.record_stop()
        self.window.destroy()

    def on_record_btn_toggled(self, button):
        self.change_record_state()

        if button.get_active():
            print("on")
            print(self.selected_index)
            self.recorder.record_start(self.selected_index)
        else:
            print("off")
            self.recorder.record_stop()
            self.add_record()

    def change_record_state(self):
        button = self.builder.get_object("record_btn")

        icon = Gtk.Image()
        label = None

        if button.get_active():
            label = "Stop"
            icon.set_from_icon_name("media-playback-stop", 0)
        else:
            label = "Record"
            icon.set_from_icon_name("media-record", 0)

        button.set_label(label)
        button.set_image(icon)

        context = button.get_style_context()
        if button.get_active():
            context.remove_class("is-active")
        else:
            context.add_class("is-active")

    def on_refresh_btn_clicked(self, _):
        self.populate_sources()

    def on_source_combo_changed(self, combo):
        if combo.get_active() == -1:
            return

        tree_iter = combo.get_active_iter()
        if tree_iter is None:
            return

        model = combo.get_model()
        self.selected_index = model[tree_iter][0]

    def populate_sources(self):
        _, clients = self.recorder.load_sink_inputs()

        self.source_store.clear()
        for index, item in clients.items():
            self.source_store.append([index, item])

        if self.source_combo.get_active() == -1:
            self.source_combo.set_active(0)

    def add_record(self):
        # TODO: delete / save
        # TODO: edit title
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        hbox.set_margin_top(10)
        hbox.set_margin_bottom(10)
        hbox.set_margin_start(10)
        hbox.set_margin_end(10)
        row.add(hbox)
        label = Gtk.Label("filename.mp3", xalign=0)
        check = Gtk.Button("Save")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(check, False, True, 0)
        self.record_list.add(row)
        self.record_list.show_all()

    def save_record(self):
        # move file
        pass
