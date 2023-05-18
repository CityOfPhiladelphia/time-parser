import pandas as pd

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

INPUT_FILE = os.getenv('INPUT_FILE')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')
print(INPUT_FILE)

meals = pd.read_csv(INPUT_FILE)

days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def checkNan( value ):
    if pd.isna(value):
        return True
    else:
        return False

def checkAMPM ( value ):
    allValues = ['AM', 'PM', 'am', 'pm', 'a.m.', 'p.m.', 'A.M.', 'P.M.']
    if checkNan(value) == False:
        if any(x in value for x in allValues):
            return True
        else:
            return False
    else:
        return False

def checkPM ( value ):
    allValues = ['PM', 'pm', 'p.m.', 'P.M.']
    if checkNan(value) == False:
        if any(x in value for x in allValues):
            return True
        else:
            return False
    else:
        return False

def checkColon ( value ):
    if checkNan(value) == False:
        if ':' in value:
            return True
        else:
            return False
    else:
        return False

def checkAll (time):
    isNan = checkNan(time)
    hasAMPM = checkAMPM(time)
    hasPM = checkPM(time)
    hasColon = checkColon(time)

    if (isNan):
        # return 'nan'
        finalTime = 'nan'
    elif (hasAMPM and hasColon):
        timeBeforeColon = time.split(':')[0]
        timeAfterColon = time.split(':')[1].split(' ')[0]
        if (hasPM):
            finalTime = str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
        else:
            finalTime = timeBeforeColon + ':' + timeAfterColon
    elif (hasAMPM and hasColon == False):
        finalTime = time.split(' ')[0]
    else:
        finalTime = time
    print(isNan, hasAMPM, hasColon, time, finalTime)

for day in days_list:
    # meals_both - split on the ampersand
    meals_both = meals[day].str.split('&', n=1, expand=True)

    meals_first = meals_both[0].str.split('-', n=1, expand=True)
    meals_second = meals_both[1].str.split('-', n=1, expand=True)

    meals_first_start = meals_first[0]
    
    for time in meals_first_start:
        checkAll(time)
        # if pd.isna(time):
        # if checkNan(time):
        #     print('time is nan:', time)

        # elif isinstance(time, float):
        #     print('time is float:', time)

        # elif ':' in time:
        #     print('time is a string, colon found in first start:', time)
        # else:
        #     # meals_first_start = meals_first_start + ':00'
        #     print('time is a string, colon not found in first start:', time)


    meals_first_end = meals_first[1]

    meals_second_start = meals_second[0]
    meals_second_end = meals_second[1]

    meals[day+'_start1']=meals_first_start
    meals[day+'_end1']=meals_first_end
    meals[day+'_start2']=meals_second_start
    meals[day+'_end2']=meals_second_end

meals.to_csv(OUTPUT_FILE)