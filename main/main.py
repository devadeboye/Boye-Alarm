"""
an alarm clock
"""
import time
import eaTime
import threading
import playsound
#from playsound import playsound

class Reminder(eaTime.Appointment):
    """

    """
    def __init__(self, g, t, l = None):
        self.__goal = g
        self.__dtime = t # due time
        self.__location = l
    
    # ----------- setters ---------
    def set_time(self, nt):
        """ nt is new time """
        self.__dtime = nt
    
    def set_goal(self, ng):
        """ ng is new goal """
        self.__goal = ng

    def set_loc(self, nl):
        """ nl is new location """
        self.__location = nl

    # ----------- getters ------------
    def get_time(self):
        return self.__dtime

    def get_goal(self):
        return self.__goal

    def get_loc(self):
        return self.__location

class Alarm(Reminder):
    """
    Class alarm is the subclass of the Reminder class.

    it contains method to calculate when the appointment
    will be due and when to sound the alarm.

    Methods include:
    ringer - plays the alarm audio file
    ring_time - calculates the time to sound the ringer
    """
    def __init__(self, g, t, f='m', l=None):
        super().__init__(g, t, l)
        '''
        f is the format of the time in either
        minutes, secs or hours)
        '''
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


class my_thread(threading.Thread):
    def __init__(self, g, t, f='m', l=None):
        threading.Thread.__init__(self)
        self.name = g # Thread name
        self.t = t # time/ duration
        self.f = f # alarm time format
        self.g = g # goal
        self.l = l # location

    def run(self):
        print("starting " + self.name)
        Alarm(self.g, self.t, self.f, self.l).run()
        print("Exiting " + self.name)







#--------------------- Test Suit ------------------
if __name__ == "__main__":
    # testing reminder
    #r1 = Reminder('buy some chips', 1)

    # test the Alarm class
    #a = Alarm('buy stat book', 10, f='s')

    # test threading
    thread1 = my_thread('10 secs test', 10, 's')
    thread2 = my_thread('20 secs test', 30, 's')
    # start the thread
    thread1.start()
    thread2.start()
    #print('Exiting main thread')