import time
from eaTime import Timing
import threading
from playsound import playsound as ring

class Alarm:
    """
    class alarm defines an alarm clock app with various functionalities.'
    """
    def __init__(self, t, title='nil'):
        try:
            self.title = title
            self.tm = t # time
        except NameError:
            print('time(t) must be a string!')

    def foo(self):
        # convert time string to secs
        self.tm = Timing().str_to_sec(self.tm)
        # get current time
        now = time.time()
        due_time = now + self.tm
        sleep_dur = due_time - now - 5
        time.sleep(sleep_dur)
        # ring if current time is equal to due_time
        if time.time() == due_time:
            ring('old-fashioned-school-bell-daniel_simon.wav')

        #/////////////////////////////////////////////////////
        # A bug is adding the no of hours inputed instead
        # of calculating what the current time is e.g
        # it added 12 hours 35 mins to the current time when
        # i set the alarm to 12:35
        #///////////////////////////////////////////////////// 


class Timer:
    """
    class Timer defines a countdown timer
    """
    def __init__(self):
        pass