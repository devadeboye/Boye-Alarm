import time
import math
import pdb

def count_down(t, f = 'm', md = 's'):
    """
        counts down from the given time. takes 3 argument.
        Takes t, f, and md as arguments
          - t = time
          - f = format (set to 'm' by default)
          - md = mode (sets to 'v' by default)

        MODE
        This determines whether the countdown timer will
        be shown or hidden.
        Mode can be 's' or 'v'
          - 's' = stealth
          - 'v' = verbose

        FORMATS
        You can specify the format(f) of t by passing:
        - 'm' for minute(s)
        - 's' for second(s)
        - 'h' for hour(s)
    """

    # validates input
    if f == 'm':
        t = Timing().ms(t)
    elif f == 'h':
        t = Timing().hs(t)
    elif f == 's':
        t = t
    # raise error when an invalid format is entered
    else:
        raise ValueError("Invalid Input! \nf can only be 'm, s or h'.")
    
    # check if time(t) is an integer, because an error will be raised
    # if it is not. so i use this to my advantage by checking if a
    # TypeError is raised 
    try:
        if md == 'v':
            while t >= 1:
                print(t)
                time.sleep(1)
                t -= 1
        elif md == 's':
            while t >= 1:
                time.sleep(1)
                t -= 1
        else: raise ValueError("mode is either 's' or 'v'!")
    except TypeError:
        #print('time (t) must be an integer!')
        raise Exception('time (t) must be an integer!')



class Timing:
    """
    Handles several calculations involving time
    """
    
    def ms(self, t):
        """ convert minute to secs -- t is time """
        return t * 60

    def mh(self, m, r = 'f'):
        """ 
        Converts minutes to hours and return the answer.
        
        When r is set to 't', returns a tuple containing
        the quotient (in hours) and the remainder (mins)
        of the convertion
        
        example: (1, 30) - this result means 1 (hour) and
        30 (mins)
        """
        if r == 'f' or r == 'F':
            return m / 60
        elif r == 't' or r == 'T':
            return divmod(m, 60)
        else:
            raise ValueError("remainder_mode should be either 'f' or 't'")

    def hs(self, h):
        """ converts hour to secs -- h is hour """
        
        return self.ms(self.hm(h))

    def hm(self, t):
        """
        converts hr(s) to min(s) -- t is time in hour(s)
        """
        
        return t * 60

    def sm(self, t, r = 'f'):
        """ converts second(s) to minute(s)
        
        Takes 2 arguments 
        t --- the time in sec(s)
        r --- remainder_mode (either 'f' or 't')

        When r is set to 't', returns a tuple containing
        the quotient (mins) and the remainder (secs) of
        the convertion
        """

        if r == 'f' or r == 'F':
            return t / 60
        elif r == 't' or r == 'T':
            return divmod(t, 60)
        else:
            raise ValueError("remainder_mode should be either 'f' or 't'")


    def sh(self, t, r = 'f'):
        """ converts second(s) to hour(s)
        
        Takes 2 arguments 
        t --- the time in sec(s)
        r --- remainder_mode (either 'f' or 't')

        When r is set to 't', returns a tuple containing
        the quotient (in hours) and the remainder (mins)
        of the convertion
        """

        if r == 'f' or r == 'F':
            return t / 3600
        elif r == 't' or r == 'T':
            return divmod(t, 3600)
        else:
            raise ValueError("remainder_mode should be either 'f' or 't'")


    def dy_2_hr(self, d):
        """ converts days to hours """
        if int(d):
            return d * 24
        raise ValueError('day must be an integer')

    def str_to_sec(self, timestring):
        """
        Accepts timestring in the format 'hh:mm' and
        converts it to secs
        """
        a = timestring.split(':')
        h = int(a[0])
        m = int(a[1])
        return (self.hs(h) + (self.ms(m)))

    def time_diff(self, t1, t2):
        """
        return the difference between two times
        """
        if(self.str_to_sec(t1) > self.str_to_sec(t2)):
            return self.str_to_sec(t1) - self.str_to_sec(t2)
        return self.str_to_sec(t2) - self.str_to_sec(t1)

    def sec_to_str(self, t):
        # ctime and time are methods in the time module
        # 
        # ctime() return string from current time in 
        # seconds from epoch
        # time() returns current time in seconds since epoch
        return time.ctime((time.time() + t))

class Appointment:

    '''
    class for appointments and tasks
    '''
    def __init__(self, t, g, l):
        self._goal = g
        self._dtime = t # due time
        self._location = l

         


#----------------------- Tests --------------------
if __name__ == '__main__' :
    #print('ms =',Timing().ms(1))
    #print('mh =',Timing().mh(150, 'f'))
    #print('hs =',Timing().hs(1))
    #print('hm =',Timing().hm(1))
    #print('sh =',Timing().sh(1))
    #print('sm =',Timing().sm(1))
    #print('dy_2_hr =',Timing().dy_2_hr(1))
    #print(Timing().sh(6000))
    #print(Timing().str_to_sec('2:30'))
    #print('time in one hour', Timing().sec_to_str(3600))

    #count_down(10, 's')
    a= Appointment(10, 'test a kit', 'home')