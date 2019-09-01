import time
from eaTime import Timing
import threading
from playsound import playsound

class Alarm:
    """
    class alarm defines an alarm clock app with various functionalities.'
    """
    def __init__(self, t, title='nil'):
        try:
            self.title = title
            # split the time string and assign it to self.tm
            self.tm = t.split(':') # time

        # when an integer is passed as a time
        except AttributeError:
            raise ValueError("""
            Time (t) must be a string, so enclose the time in '' separating
            the hours and mins with a colon (:). e.g '12:00'
            """)

        # when time is not enclosed in a quote
        except SyntaxError:
            raise ValueError('invalid input! time(t) and title must be a string.')

        # when the title is not surrounded with a quote
        except NameError:
            raise ValueError('title must be a string!')

    def proc(self):
        """
        contains all process that keep record of the alarm/reminder
        """
        # get current time as a tuple
        now = time.localtime()

        # compare current time with the entered time
        # 
        # if current time (h) > due time (h)
        if now[3] > int(self.tm[0]):
            raise ValueError('invalid time! That time has passed.')

        # hour is the same, but mins is lesser than current mins
        elif now[3] == int(self.tm[0]) and now[4] > int(self.tm[1]):
            raise ValueError('invalid time! That time has passed.')

        # hour and mins are equal
        elif now[3] == int(self.tm[0]) and now[4] == int(self.tm[1]):
            sleep_dur = 0
        # if current time > due time
        else:
            # compare the time
            h = int(self.tm[0]) - now[3] #hour
            m = int(self.tm[1]) - now[4] #minutes
            # convert h and m to seconds
            sleep_dur = Timing().hs(h) + Timing().ms(m)

        # Tell the user when the alarm will sound
        if sleep_dur < 60:    
            print(f"Alarm will sound in {sleep_dur} second(s) time")

        elif sleep_dur > 60 and sleep_dur < 3600:
            st = Timing().sm(sleep_dur, r='t') #sleep time
            print(f"Alarm will sound in {st[0]} min(s) {st[1]} seconds time")
            
        elif sleep_dur > 3600:
            st = Timing().sh(sleep_dur, r='t')
            print(f"Alarm will sound in {st[0]} hour(s) {st[1]} min(s) time")
        
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


class Timer:
    """
    class Timer defines a countdown timer
    """
    def __init__(self):
        pass





# ---------------- test -------------
if __name__ == "__main__":
    Alarm('13:58', 'test').start()