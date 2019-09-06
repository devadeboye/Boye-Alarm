import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import json
import alarm

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pagus")
        self.set_border_width(3)

        # container to hold all item
        main_container = Gtk.HBox()
        # add container to main window
        self.add(main_container)


        #-------- SIDE BAR -----------
        # grid to hold sidebar buttons
        self.sidebar = Gtk.Grid()
        # button to add an alarm
        add_but = Gtk.Button(label='Add Alarm')
        # connect button to its command function
        add_but.connect('clicked', self.show_add_page)
        # button to lauch info about the app
        about = Gtk.Button(label='About')
        about.connect('clicked', self.about_app)

        # add both buttons to grid
        self.sidebar.add(add_but)
        self.sidebar.attach(about, 0, 1, 1, 1)
        # add sidebar to main_container
        main_container.pack_start(self.sidebar, True, True, 0)
        
        # page to display list of alarms
        self.alarm_page = Gtk.ListBox()
        # set border width of the 1st page
        self.alarm_page.set_border_width(10)

        # ----------- PAGE 1 ---------------
        try:
            # open file for reading
            fr = open("record.json", "r")
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
                self.alarm_page.add(s)

            else:
                #iterate over the alarm dictionary
                for k, v in alarm_data.items():
                    try:
                        # try to set each alarm
                        alarm.AlarmThread(k,v).start()
                        # create a label for each entry
                        l = Gtk.Label()

                        # left justification
                        l.set_justify(Gtk.Justification.LEFT)

                        # style the text using pango markup
                        l.set_markup(f"<span size='x-large'><b>{k}</b></span>\n<small>{v}</small>")
                        
                        # add content to the listbox
                        self.alarm_page.add(l)
                    # if time is invalid
                    except Exception as error:
                        temp.append(k)
                        print(error)
                        #print('Heck NOoooo!')

                # remove invalid/ expired entries
                for el in temp:
                    del(alarm_data[el])
                # open file for writing
                fw = open('record.json', 'w')
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
            self.alarm_page.add(r)

        # add page 1 to stack ---->
        main_container.pack_start(self.alarm_page, True, True, 0)


    def show_add_page(self):
        cont = Gtk.Grid()
        time_label = Gtk.Label('Time')
        time = Gtk.Entry()

        title_label = Gtk.Label('Title')
        title = Gtk.Entry()

        submit = Gtk.Button(label='submit')
        #submit.connect('clicked', alarm.add_alarm(time, title))
        
        cont.add(time_label)
        cont.attach(time, 1, 0, 1, 1)
        cont.attach(title_label, 0, 1, 1, 1)
        cont.attach(title, 1, 1, 1, 1)
        cont.attach(submit, 0, 2, 1, 1)


    def about_app(self):
        info = Gtk.AboutDialog()


# create an instance of my window
win = MyWindow()
# connect to the window's delete event
win.connect("destroy", Gtk.main_quit)
# display the window
win.show_all()
# start the GTK+ processing loop
Gtk.main()