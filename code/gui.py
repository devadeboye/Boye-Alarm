import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import json

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pagus")
        self.set_border_width(3)

        # create the stack container
        stack_cont = Gtk.VBox()
        # add container to main window
        self.add(stack_cont)
        # create the stack
        stack = Gtk.Stack()
        #self.add(self.stack)
        # create page 1
        self.page1 = Gtk.ListBox()
        # set border width of the 1st page
        self.page1.set_border_width(10)

        # ----------- PAGE 1 ---------------
        try:
            # open file for reading
            fr = open('alarms.json', 'r')
            # load data
            self.alarm_data = json.load(fr)
        except FileNotFoundError:
            print('wahala here!') # display that no alarm is set yet

        #iterate over the content of the dictionary
        for k, v in self.alarm_data.items():
            # sample content which i will later delete
            l = Gtk.Label()
            l.set_justify(Gtk.Justification.LEFT)
            l.set_markup(f"<span size='x-large'><b>{k}</b></span>\n<small>{v}</small>")
            # add content to the listbox
            self.page1.add(l)

        
        

        # add page 1 to stack
        stack.add_titled(self.page1, 'Alarm', 'Alarm')

        # create page 2
        self.page2 = Gtk.Box()
         # set border width of the 2nd page
        self.page2.set_border_width(10)
        stack.add_titled(self.page2, 'About','About')

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        stack_cont.pack_start(stack_switcher, False, False, 0)
        stack_cont.pack_start(stack, False, False, 0)


# create an instance of my window
win = MyWindow()
# connect to the window's delete event
win.connect("destroy", Gtk.main_quit)
# display the window
win.show_all()
# start the GTK+ processing loop
Gtk.main()