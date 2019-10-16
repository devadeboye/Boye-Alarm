
def get_platform():
    """
    Gets the operating system of the device its running on.
    """
    import sys
    import os

    platforms = {'linux1' : 'Linux','linux2' : 'Linux',\
        'darwin' : 'OS X', 'win32' : 'Windows'}
    
    if sys.platform not in platforms:
        if 'ANDROID_ARGUMENT' in os.environ:
            return 'Android'
        return sys.platform
    return platforms[sys.platform]
    
    
    
    
#-------------------------------------------
if __name__=="__main__":
    print(get_platform())
    