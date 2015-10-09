# https://stackoverflow.com/questions/1557571/how-to-get-time-of-a-python-program-execution/
import atexit
from time import clock
from datetime import timedelta

def secondsToStr(t):
    return str(timedelta(seconds=t))

line = "="*40
def log(s, elapsed=None):
    print(line)
    print(secondsToStr(clock()), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()

def endlog(start):
    end = clock()    
    elapsed = end-start
    log("End Program", secondsToStr(elapsed))
	
def startlog():
    start = clock()
    log("Start Program")    
    return start

def now():
    return secondsToStr(clock())

