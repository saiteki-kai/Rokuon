from gi.repository import Gtk


class DestroyDialog(Gtk.Dialog):
    def __init__(self, parent, message):
        Gtk.Dialog.__init__(self, title="Delete", transient_for=parent, flags=0)

        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_DELETE, Gtk.ResponseType.OK
        )

        self.set_default_size(400, 100)

        label = Gtk.Label(label="Are you sure you want to delete {}?".format(message))
        label.set_vexpand(True)

        box = self.get_content_area()
        box.add(label)

        self.show_all()
