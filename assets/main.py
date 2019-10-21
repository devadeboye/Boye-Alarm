#!/usr/bin/python3

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
#import alarm
import sqlite3
import time as time_module
import getOs
import os
from eaTime import Timing
from threading import Timer
from playsound import playsound

def ring():
    """
    ring if current time is equal to due_time
    """
    playsound('old-fashioned-school-bell-daniel_simon.wav')

class InvalidInputError(Exception):
    """
    Thrown when an unexpected input was given
    """
    pass
        

class TimePassedError(Exception):
    """
    Thrown when time has elapsed
    """
    pass
        

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

        #-------- menu section starts here -------
        #  
        # create a menubutton
        menu_but = Gtk.MenuButton()
        # create a popover
        popover = Gtk.Popover()

        # create a grid to hold the popover item
        popover_grid = Gtk.Grid()
        # popover items
        about_but = Gtk.Button('About')
        # connect button to callback function
        about_but.connect('clicked', self.about_app)
        # add about button to the grid
        popover_grid.add(about_but)
        popover_grid.show_all()

        # add grid to popover
        popover.add(popover_grid)
        # set popover to be shown when menu button is clicked
        menu_but.set_popover(popover)

        # add menubutton to headerbar
        headerbar.pack_end(menu_but)
        #----------- menu section ends here ----------


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
        self.inner_container = Gtk.VBox()
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

        # add input section to the inner container
        self.inner_container.pack_start(self.input_section, False, True, 10)

        # add inner container to the main container
        self.main_container.pack_start(self.inner_container, True, True, 0)       

        # show all schedules if any
        self.show_and_set_alarms()


    def new_alarm(self, widget):
        """
        Method to create a new alarm
        """
        # capture user's entry
        self.time_content = str(self.time.get_text())
        self.title_content =str(self.title.get_text())

        # get current time as a tuple
        now = time_module.localtime()

        #--------- input validation codes -----------
        test_time = ''
        test_time += self.time_content
        # check if valid time format was entered
        if len(test_time.split(':')) != 2:
            print('the length is', len(test_time.split(':')))
            raise InvalidInputError('Enter time separated by (:) e.g 10:00')
            #raise ValueError('Enter time separated by (:) e.g 10:00')
        else:
            # split the time string and assign it to test_time
            test_time = test_time.split(':')
            # check if hours is valid
            if len(test_time[0]) > 2 or len(test_time[0]) < 1:
                test_time = None
                raise InvalidInputError('Invalid input for hour!')
            # check if minute is valid
            elif len(test_time[1]) != 2:
                self.tm = None
                raise InvalidInputError('Invalid input for minute!')
            # min or secs must be < 60
            elif int(test_time[1]) > 60:
                raise InvalidInputError('Mins or Secs must be less than 60')
            # if current time (h) > due time
            elif now[3] > int(test_time[0]):
                raise TimePassedError("That time has passed!")

            # hour is the same, but mins is lesser than current mins
            elif now[3] == int(test_time[0]) and now[4] >\
                int(test_time[1]):
                raise TimePassedError("That time has passed!")

        #------- validation codes ends here ---------
        print(f'This is what i wanna save {self.time_content}\n\n')
        
        # get the name of the current logged in user
        logged_in_user = os.getlogin()

        # check if directory exist
        try:
            if getOs.get_platform() == 'linux':
                # create a db
                db = sqlite3.connect(f'/home/{logged_in_user}/Documents/.BoyeAlarm/alarm_records.db')
            elif getOs.get_platform() == 'Windows':
                # create a db
                db = sqlite3.connect(f'C:/users/{logged_in_user}/.BoyeAlarm/alarm_records.db')
        
            # get a cursor object
            cur = db.cursor()
            # create a table if it doesn't exist
            cur.execute(""" CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, time TEXT, title TEXT) """)
            # add alarm info to db
            cur.execute(""" INSERT INTO schedules (time, title) VALUES (?, ?)""", (self.time_content, self.title_content))
            # commit changes
            db.commit()
            # close the db
            db.close()

            print('alarm added')

            # delete and reload the listbox
            self.scrolled_window.destroy()
            # clear the content of the  entry boxes
            self.time.set_text('')
            self.title.set_text('')
            # show all schedules if any
            self.show_and_set_alarms()
        except sqlite3.OperationalError:
            # check for os type
            if getOs.get_platform() == 'linux':
                # create a directory
                os.mkdir(f'/home/{logged_in_user}/Documents/.BoyeAlarm/')
                # create a db
                db = sqlite3.connect(f'/home/{logged_in_user}/Documents/.BoyeAlarm/alarm_records.db')
            elif getOs.get_platform() == 'Windows':
                # create a directory
                os.mkdir(f'C:/users/{logged_in_user}/.BoyeAlarm/')
                # create a db
                db = sqlite3.connect(f'C:/users/{logged_in_user}/.BoyeAlarm/alarm_records.db')

            # save the alarm details to db
            #db = sqlite3.connect('alarm_records.db')
            # get a cursor object
            cur = db.cursor()
            # create a table if it doesn't exist
            cur.execute(""" CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, time TEXT, title TEXT) """)
            # add alarm info to db
            cur.execute(""" INSERT INTO schedules (time, title) VALUES (?, ?)""", (self.time_content, self.title_content))
            # commit changes
            db.commit()
            # close the db
            db.close()

            print('alarm added')

            # delete and reload the listbox
            self.scrolled_window.destroy()
            # clear the content of the  entry boxes
            self.time.set_text('')
            self.title.set_text('')
            # show all schedules if any
            self.show_and_set_alarms()


    def show_and_set_alarms(self):
        """
        start the available alarms and show them in the
        GUI
        """
        # scrolled window to hold the listbox
        self.scrolled_window = Gtk.ScrolledWindow()
        # create a listbox to hold the alarm schedules
        self.gui_alarm_info = Gtk.ListBox()
        # add listbox to scrolled window
        self.scrolled_window.add(self.gui_alarm_info)
        # add scrolled window to inner container
        self.inner_container.pack_start(self.scrolled_window, True, True, 10)

        # get current time
        now = time_module.localtime()

#----------------------------------------------------------

        # get the name of the current logged in user
        logged_in_user = os.getlogin()

        # check if directory exist
        try:
            if getOs.get_platform() == 'linux':
                # create a db
                db = sqlite3.connect(f'/home/{logged_in_user}/Documents/.BoyeAlarm/alarm_records.db')
            elif getOs.get_platform() == 'Windows':
                # create a db
                db = sqlite3.connect(f'C:/users/{logged_in_user}/.BoyeAlarm/alarm_records.db')

            # get cursor object
            cur = db.cursor()
            # check db for records
            try:
                cur.execute('SELECT * FROM schedules')
                db.commit()
                schedules = cur.fetchall()
                #print(schedules) #---->
                
                # empty set to hold items that are to be deleted
                to_be_deleted = set()

                # gather expired items in schedule by id and
                # delete them from the db
                for n in schedules:
                    aa = n[1].split(':')
                    if now[3] > int(aa[0]):
                        to_be_deleted.add(n[0])
                        print(f'{now[3]} <<------>> {int(aa[0])} ------ {n}') #---->
                    if now[3] == int(aa[0]) and now[4] > int(aa[1]):
                        to_be_deleted.add(n[0])
                        print(f'{now[3]} ---------- {aa[1]}') #---->
                print(f'\n\n These items are to be deleted\n {to_be_deleted}\n\n') #---->

                # delete expired items
                for identity in to_be_deleted:
                    cur.execute('DELETE FROM schedules WHERE id = ?', (identity,))
                db.commit()

                # recollect items from the db
                cur.execute('SELECT * FROM schedules')
                valid_schedules = cur.fetchall()
                print(valid_schedules) #---->
            except Exception:
                # create a table if it doesn't exist
                cur.execute(""" CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, time TEXT, title TEXT) """)
                db.commit()
                return(0)

            for item in valid_schedules:
                #------ start of code calculating wait time -------
                # get current time as a tuple
                now = time_module.localtime()
                # split the time string for easy calculation
                alarm_time = item[1].split(':')
                # compare current time with alarm time
                #
                # hour and mins are equal
                if now[3] == int(alarm_time[0]) and now[4] ==\
                    int(alarm_time[1]):
                    # set sleep duration to zero
                    sleep_dur = 0
                # if current time > due time
                else:
                    # compare the time
                    h = int(alarm_time[0]) - now[3] # hour
                    m = int(alarm_time[1]) - now[4] # minutes
                    # convert h and m to seconds
                    sleep_dur = Timing().hs(h) + Timing().ms(m)
                #------ end of code calculating wait time -----
                
                # run action in a thread
                Timer(sleep_dur, ring).start()
                # set the alarm
                #alarm.AlarmThread(item[1], item[2]).start()

                l = Gtk.Label()
                # left justification
                l.set_justify(Gtk.Justification.LEFT)
                # horizontal alignment of the text in the label
                l.set_xalign(0)

                # style the text using pango markup
                l.set_markup(f"<span size='x-large'><b>{item[1]}</b></span>\n<small>{item[2]}</small>")
                # add show alarm info in gui
                self.gui_alarm_info.add(l)
            
            # close the db
            db.close()

            # show the listbox
            self.scrolled_window.show_all()
          
        except sqlite3.OperationalError:
            # check for os type
            if getOs.get_platform() == 'linux':
                # create a directory
                os.mkdir(f'/home/{logged_in_user}/Documents/.BoyeAlarm/')
                # create a db
                db = sqlite3.connect(f'/home/{logged_in_user}/Documents/.BoyeAlarm/alarm_records.db')
            elif getOs.get_platform() == 'Windows':
                # create a directory
                os.mkdir(f'C:/users/{logged_in_user}/.BoyeAlarm/')
                # create a db
                db = sqlite3.connect(f'C:/users/{logged_in_user}/.BoyeAlarm/alarm_records.db')


    def about_app(self, widget):
        info = Gtk.AboutDialog()
        info.set_transient_for(self)
        info.set_program_name('Boye Alarm')
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