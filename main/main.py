"""
an alarm clock
"""
import time
import eaTime
import threading
import playsound
#from playsound import playsound

class CountDown(eaTime.Reminder):
    """
    Class CountDown is the subclass of the Reminder class.

    it contains method that calculate when the timer will
    run out and sound the alarm at an appropriate time.

    Methods include:
    ringer - plays an audio file when the timer runs out
    ring_time - calculates the time to sound the ringer
    """
    def __init__(self, g, t, f='m', l=None):
        super().__init__(g, t, l)
        """
        - f is the format of the time in either
          minutes, secs or hours)
        - g = goal/purpose of the countdown
        - t = due time
        """
        self.tf = f #time format

    def __ringer(self):
        """
        plays the alarm audio file
        """
        playsound.playsound('old-fashioned-school-bell-daniel_simon.wav')
        

    def __ring_time(self):
        """
        calculates the time to sound the ringer
        """
        eaTime.count_down(self.get_time(), self.tf)
        print(self.get_goal())
        self.__ringer()

    def run(self):
        """
        starts the app
        """
        self.__ring_time()


class CountDownThread(threading.Thread):
    """
    A class that allow us to run more than one instance
    of the CountDown class concurrently
    """
    def __init__(self, g, t, f='m', l=None):
        threading.Thread.__init__(self)
        self.name = g # Thread name/label
        self.t = t # time/ duration
        self.f = f # alarm time format
        self.g = g # goal
        self.l = l # location

    def run(self):
        print("starting " + self.name)
        CountDown(self.g, self.t, self.f, self.l).run()
        print("Exiting " + self.name)







#--------------------- Test Suit ------------------
if __name__ == "__main__":
    # testing reminder
    #r1 = Reminder('buy some chips', 1)

    # test the Alarm class
    #a = Alarm('buy stat book', 10, f='s')

    # test threading
    thread1 = CountDownThread('10 secs test', 10, 's')
    thread2 = CountDownThread('20 secs test', 20, 's')
    # start the thread
    thread1.start()
    thread2.start()
    #print('Exiting main thread')