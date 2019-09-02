import time
from eaTime import Timing
import threading
from playsound import playsound
import json
import sqlite3
import os

class Alarm:
    """
    class alarm defines an alarm clock app with various
    functionalities.'
    """
    def __init__(self, t, title='nil'):
        try:
            self.title = title
            # split the time string and assign it to self.tm
            self.tm = t.split(':') # time

        # when an integer is passed as a time
        except AttributeError:
            raise ValueError("Time (t) must be a string"+\
                ", so enclose the time in '' separating"+\
                    " the hours and mins with a colon "+\
                        "(:). e.g '12:00'")

        # when time is not enclosed in a quote
        except SyntaxError:
            raise ValueError("invalid input! time(t) "+\
                "and title must be a string.")

        # when the title is not surrounded with a quote
        except NameError:
            raise ValueError('title must be a string!')

    def proc(self):
        """
        contains all process that keep record of the
        alarm/reminder
        """
        # get current time as a tuple
        now = time.localtime()

        # compare current time with the entered time
        #
        # if min or secs > 59
        if int(self.tm[1]) > 59:
            raise ValueError("invalid time!")
        # if current time (h) > due time
        elif now[3] > int(self.tm[0]):
            raise ValueError("invalid time! That time "+\
                "has passed.")

        # hour is the same, but mins is lesser than current mins
        elif now[3] == int(self.tm[0]) and now[4] >\
            int(self.tm[1]):
            raise ValueError("invalid time! That time "+\
                "has passed.")

        # hour and mins are equal
        elif now[3] == int(self.tm[0]) and now[4] ==\
            int(self.tm[1]):
            # set sleep duration to zero
            sleep_dur = 0
        # if current time > due time
        else:
            # compare the time
            h = int(self.tm[0]) - now[3] #hour
            m = int(self.tm[1]) - now[4] #minutes
            # convert h and m to seconds
            sleep_dur = Timing().hs(h) + Timing().ms(m)

        #----------- INFORM USERS OF WAIT TIME --------
        # sleep duration less than 60 secs
        if sleep_dur < 60:
            # Tell the user when the alarm will sound  
            print(f'Alarm will sound in {sleep_dur} '+\
                'second(s) time')

        # sleep duration > 60 secs and < 3600
        elif sleep_dur >= 60 and sleep_dur < 3600:
            #sleep time
            st = Timing().sm(sleep_dur, r='t')
            # Tell the user when the alarm will sound
            print(f'Alarm will sound in {st[0]} min(s)'+\
                ' {st[1]} seconds time')
            
        # sleep duration > 3600
        elif sleep_dur >= 3600:
            #sleep time
            st = Timing().sh(sleep_dur, r='t')
            # Tell the user when the alarm will sound
            print(f"Alarm will sound in {st[0]} hour(s)"+\
                " {st[1]} min(s) time")
        
        # sleep till its time to sound the alarm
        time.sleep(sleep_dur)
        
    def ring(self):
        """
        ring if current time is equal to due_time
        """
        playsound('old-fashioned-school-bell-daniel_simon.wav')

    def start(self):
        """
        a method to start the alarm
        """
        # process the time
        self.proc()
        # call the ringer
        self.ring()


class AlarmThread(threading.Thread):
    """
    Makes running the Alarm class possible. it accepts
    two arguments:

    PARAMETERS
    t = time alarm should sound
    title = title or name for the task/alarm
    """

    def __init__(self, t, title):
        """
        constructor for AlarmThread class.
        t - stands for time(t)
        title - is the title of the alarm
        """
        threading.Thread.__init__(self)
        self.time = t
        self.title = title

    def run(self):
        print(f'starting {self.title}!')
        Alarm(self.time, self.title).start()
        print(f'exiting {self.title}!')


def add_alarm(t,title='nil'):
    """
    collects all necessary info needed to set the
    alarm from the user.

    PARAMETERS
    t = time alarm should sound
    title = title or name for the task/alarm
    """
    try:
        # open file for reading
        fr = open('alarms.json', 'r')
        # load data
        alarm_data = json.load(fr)

        # add item to the dict
        alarm_data[t] = title
        # open file to write changes
        fw = open('alarms.json', 'w')

        # write the changes to file
        json.dump(alarm_data, fw, indent=4)
        # close file
        fw.close()

    except FileNotFoundError:
        fw = open('alarms.json', 'w')
        json.dump({t:title}, fw, indent=4)
        fw.close()





# ---------------- test -------------
if __name__ == "__main__":
    #AlarmThread('11:60', 't1').start()
    #AlarmThread('11:21', 't2').start()
    add_alarm('2:30','cook')
   