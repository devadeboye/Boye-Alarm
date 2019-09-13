#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import json
import alarm
import sqlite3

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(3)
        #self.set_decorated(False)
        # set windows default size
        self.set_default_size(450, 250)
        # make window unresizeable
        self.set_resizable(False)

        # create a headerbar
        headerbar = Gtk.HeaderBar()
        # set the headerbar as the titlebar of the window
        self.set_titlebar(headerbar)
        # set the title of the header bar
        headerbar.set_title('Boye Alarm')
        # show close button
        headerbar.set_show_close_button(True)

        # create a menubutton
        menu_but = Gtk.MenuButton()

        # menu to be popped when menubutton is clicked
        menu = Gtk.Menu()
        # create a menu item
        menu_item = Gtk.MenuItem()
        # menu items are listed below
        about = Gtk.Label('About')
        # add items to menu item
        #menu_item.add(about)
        # add menu items to menu
        menu.add(menu_item)

        # popover
        popover = Gtk.Popover()
        popover.add(about)
        popover.set_relative_to(menu_but)
        


        # set the menu that will be popped when clicked
        menu_but.set_popover(popover)
        # add menubutton tto headerbar
        headerbar.pack_end(menu_but)


        #---------- App's body section ---------
        #  
        # container to hold all item
        self.main_container = Gtk.VBox()
        # add container to main window
        self.add(self.main_container)

        # variable to hold time and title of alarm
        self.title = self.time = self.time_content =\
            self.title_content = None
        
        # add inner section of the app
        inner_container = Gtk.VBox()
        # create grid to hold the input section
        self.input_section = Gtk.Grid()

        # items of the input section
        self.time = Gtk.Entry()
        self.title = Gtk.Entry()
        submit = Gtk.Button('Add')
        submit.connect("clicked", self.new_alarm)

        # set the size of the entry box
        self.time.set_width_chars (45)
        self.title.set_width_chars (45)

        # add placeholder for time and title
        self.time.set_placeholder_text('Enter Time')
        self.title.set_placeholder_text('Enter Title')

        # add input items to grid
        self.input_section.attach(self.time, 0, 0, 2, 1)
        self.input_section.attach(self.title, 0, 1, 2, 1)
        self.input_section.attach(submit, 2, 0, 1, 2)

        # create a listbox to display the alarm info
        self.gui_alarm_info = Gtk.ListBox()

        # add input section to the inner container
        inner_container.pack_start(self.input_section, False, True, 10)
        # add gui_alarm_info to inner container
        inner_container.pack_start(self.gui_alarm_info, True, True, 10)

        # add inner container to the main container
        self.main_container.pack_start(inner_container, True, True, 0)

        

        # show all schedules if any
        self.show_and_set_alarms()


    def new_alarm(self, widget):
        """
        Method to create a new alarm
        """
        # capture user's entry
        self.time_content = str(self.time.get_text())
        self.title_content =str(self.title.get_text())

        #--------- input validation codes -----------
        wwwww

        # save the alarm details to db
        db = sqlite3.connect('alarm_records.db')
        # get a cursor object
        cur = db.cursor()
        # create a table if it doesn't exist
        cur.execute(""" CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, time TEXT, title TEXT) """)
        # add alarm info to db
        cur.execute(""" INSERT INTO schedules (time, title) VALUES (?, ?)""", (self.time_content, self.title_content))
        # commit changes
        db.commit()

        print('alarm added')

        # show all schedules if any
        self.show_and_set_alarms()


    def show_and_set_alarms(self):
        """
        show the list of alarms in record
        """
        # connect to the db
        db = sqlite3.connect('alarm_records.db')
        # get cursor object
        cur = db.cursor()
        # check db for records
        try:
            cur.execute('SELECT * FROM schedules')
            db.commit()
            schedules = cur.fetchall()
            print(schedules)
        except Exception:
            # create a table if it doesn't exist
            cur.execute(""" CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, time TEXT, title TEXT) """)
            db.commit()
            return(0)

        for item in schedules:
            try:
                # set the alarm
                alarm.AlarmThread(item[1], item[2]).start()

                l = Gtk.Label()
                # left justification
                l.set_justify(Gtk.Justification.LEFT)

                # style the text using pango markup
                l.set_markup(f"<span size='x-large'><b>{item[1]}</b></span>\n<small>{item[2]}</small>")
                # add show alarm info in gui
                self.gui_alarm_info.add(l)
        


    def about_app(self, widget):
        info = Gtk.AboutDialog()
        info.set_transient_for(self)
        info.set_program_name('Pagus')
        info.set_version('1.0')
        info.set_comments ('An alarm clock app for PC')
        info.set_copyright('Copyright © 2019 Emmanuel Adeboye')
        info.set_authors (['Adeboye Emmanuel'])
        info.add_credit_section ('Appreciation:',\
            ['Adeboye Elijah',
            'Adeboye Cecilia',
            'Kayode Okanlawon',
            'Oniyide Hanameel'])

        # start the dailog
        info.run()
        info.destroy()


# create an instance of my window
win = MyWindow()
# connect to the window's delete event
win.connect("destroy", Gtk.main_quit)
# display the window
win.show_all()
# start the GTK+ processing loop
Gtk.main()




#/////////////////////////////////////////////

# TASK ADDING ALGORITHM
# ------------------------ 
# - accept the parameters
# - if parameters are valid:
#     - write the input from users into db
#     - call on function to update the UI 
# - else:
#     - raise an exception via a popup box stating
#       the error.
# 
# 
# ALGORITHM TO CONTROL WHAT TO DO ON LAUNCH
# -----------------------------------------
# - if there are item in the db:
#     - load them
#     - set alarm for them
#     - add their alarm info to the gui
# - else:
#     - raise alarm empty error as a popup
# 
# 
# ALARM TRIGGER ALGORITHM
# - if time == specified time:
#     - sound the alarm
#     - remove alarm info from gui
#     - remove alarm record from db
# - else:
#     - sleep till its time
#