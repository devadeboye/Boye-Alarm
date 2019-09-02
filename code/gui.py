import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import json
import alarm

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
            alarm_data = json.load(fr)
            fr.close()
            # contains invalid times
            temp = []

            # if no alarm set
            if len(alarm_data) < 1:
                # create label for the error message
                s = Gtk.Label()
                s.set_justify(Gtk.Justification.LEFT)
                
                # error message
                msg = "you have set no alarm!"
                # style the text using pango markup
                s.set_markup(f"<span size='small'>{msg}</span>")
                
                # add content to the listbox
                self.page1.add(s)

            #iterate over the content of the dictionary
            for k, v in alarm_data.items():
                try:
                    # set the alarm
                    assert(alarm.AlarmThread(k,v).start())
                    # create a label for each entry
                    l = Gtk.Label()

                    # left justification
                    l.set_justify(Gtk.Justification.LEFT)

                    # style the text using pango markup
                    l.set_markup(f"<span size='x-large'><b>{k}</b></span>\n<small>{v}</small>")
                    
                    # add content to the listbox
                    self.page1.add(l)
                except:
                    temp.append(k)
                    print('Heck NOoooo!')

            # remove invalid/ expired entries
            for el in temp:
                del(alarm_data[el])
            # open file for writing
            fw = open('alarms.json', 'w')
            json.dump(alarm_data, fw, indent=4)
            fw.close()
            

        except FileNotFoundError:
            # create label for the error message
            r = Gtk.Label()
            r.set_justify(Gtk.Justification.LEFT)
            
            # error message
            msg = "You are yet to set an alarm"
            # style the text using pango markup
            r.set_markup(f"<span size='small'>{msg}</span>")
            
            # add content to the listbox
            self.page1.add(r)

        # add page 1 to stack
        stack.add_titled(self.page1, 'Alarm', 'Alarm')

        #-------------- PAGE 2 ---------------------
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