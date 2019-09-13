#!/usr/bin/python3

import time
from eaTime import Timing
import threading
from playsound import playsound
import sqlite3
import os

class InvalidInputError(Exception):
    def __init__(self):
        """
        Thrown when an unexpected input was given
        """
        Exception.__init__(self)
        

class TimePassedError(Exception):
    def __init__(self):
        """
        Thrown when time has elapsed
        """
        Exception.__init__(self)
        

class Alarm:
    """
    class alarm defines an alarm clock app with various
    functionalities.'
    """
    def __init__(self, t, title):
        self.title = title
        self.tm = t

    def proc(self):
        """
        contains all process that keep record of the
        alarm/reminder
        """
        # get current time as a tuple
        now = time.localtime()
        # split the time string and assign it to self.time_content
        self.tm = self.tm.split(':')

        # compare current time with the entered time
        #
        # hour and mins are equal
        if now[3] == int(self.tm[0]) and now[4] ==\
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
                f' {st[1]} seconds time')
            
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
        a = Alarm(self.time, self.title)
        # process the time
        a.proc()
        # call the ringer
        a.ring()
        print(f'exiting {self.title}!')








# ---------------- test -------------
if __name__ == "__main__":
    AlarmThread('20:02', 't1').start()
    AlarmThread('19:59', 't2').start()
    