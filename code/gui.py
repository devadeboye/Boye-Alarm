import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import json
import alarm

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Pagus")
        self.set_border_width(3)
        # set windows default size
        self.set_default_size(500, 200)
        # make window unresizeable
        self.set_resizable(False)

        # container to hold all item
        self.main_container = Gtk.HBox()
        # add container to main window
        self.add(self.main_container)

        # variable to hold time and title of alarm
        self.title = self.time = self.time_content =\
            self.title_content = None
        
        #/////////////////////////////////////////////

        # TASK ADDING ALGORITHM
        # ------------------------ 
        # - accept the parameters
        # - if parameters are valid:
        #     - set the alarm with the parameters
        #     - add the alarm info to the gui
        #     - add the alarm info to the db
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


        #/////////////////////////////////////////////

        


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