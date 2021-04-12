import os
from gi.repository import Gtk

from rokuon.pulse_recorder import Recorder
from rokuon.utils import get_file_duration, get_file_size
from rokuon.constants import ui_directory, save_directory

from rokuon.widgets.new_record import NewRecord
from rokuon.widgets.record_item import RecordItem

UI_MAIN_WINDOW = os.path.join(ui_directory, "main_window.ui")
UI_MENUBAR = os.path.join(ui_directory, "menubar.ui")


class MainWindow:
    def __init__(self, app=None):
        self.app = app

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_MAIN_WINDOW)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.window.set_application(self.app)

        # Setup Menu
        self.builder.add_from_file(UI_MENUBAR)
        menu_btn = self.builder.get_object("menu_btn")
        menu = self.builder.get_object("app-menu")
        menu_btn.set_menu_model(menu)

        self.selected_index = None
        self.recorder = Recorder()

        self.record_btn = self.builder.get_object("record_btn")
        self.record_list = self.builder.get_object("record_list")
        self.source_store = self.builder.get_object("source_store")
        self.source_combo = self.builder.get_object("source_combo")

        self.source_combo.set_active(0)
        self.on_refresh_btn_clicked()

        self.change_record_state()
        self.update_source_list()

    def show(self):
        self.window.show_all()

    def destroy(self, _):
        self.recorder.record_stop()
        self.window.destroy()

    def on_record_btn_toggled(self, button):
        self.change_record_state()

        if button.get_active():
            try:
                self.recorder.record_start(self.selected_index, "mp3")
            except RuntimeError as err:
                print(err)
                button.set_active(True)
                self.change_record_state()
        else:
            self.recorder.record_stop()
            self.add_record()

    def change_record_state(self):
        icon = Gtk.Image()

        if self.record_btn.get_active():
            label = "Stop"
            icon.set_from_icon_name("media-playback-stop", 0)
        else:
            label = "Record"
            icon.set_from_icon_name("media-record", 0)

        self.record_btn.set_label(label)
        self.record_btn.set_image(icon)

        context = self.record_btn.get_style_context()
        if self.record_btn.get_active():
            context.remove_class("is-active")
        else:
            context.add_class("is-active")

    def on_refresh_btn_clicked(self, _=None):
        self.populate_sources()

        # Enable or disable the record button
        enable = len(self.source_store) > 0
        self.record_btn.set_sensitive(enable)
        # TODO: style disabled record button

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
        self.source_combo.set_active(-1)
        for index, item in clients.items():
            self.source_store.append([index, item])

        if self.source_combo.get_active() == -1:
            self.source_combo.set_active(0)

    def add_record(self):
        row = NewRecord(save_cb=self.on_save)
        self.record_list.add(row)
        self.record_list.show_all()

    def update_source_list(self):
        for child in self.record_list.get_children():
            self.record_list.remove(child)

        for file in os.listdir(save_directory):
            filepath = os.path.join(save_directory, file)

            duration = get_file_duration(filepath)
            size = get_file_size(filepath)

            item = RecordItem(file, duration, size, delete_cb=self.on_delete)
            self.record_list.add(item)
        self.record_list.show_all()

    def on_save(self):
        self.update_source_list()

    def on_delete(self, filename):
        filepath = os.path.join(save_directory, filename)
        # TODO: add confirm dialog
        os.remove(filepath)
        self.update_source_list()
