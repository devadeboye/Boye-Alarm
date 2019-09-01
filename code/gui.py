import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pagus")


# create an instance of my window
win = MyWindow()
# connect to the window's delete event
win.connect("destroy", Gtk.main_quit)
# display the window
win.show_all()
# start the GTK+ processing loop
Gtk.main()