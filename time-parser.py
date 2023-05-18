import pandas as pd

import os
from dotenv import load_dotenv
from pathlib import Path
import re

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
        finalTime = ''
    elif (hasAMPM and hasColon):
        timeBeforeColon = time.split(':')[0].strip()
        timeAfterColonWithAMPM = time.split(':')[1]
        timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
        if (hasPM):
            if int(timeBeforeColon) == 12:
                finalTime = '12:' + timeAfterColon
            else:
                finalTime = str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
        else:
            finalTime = timeBeforeColon + ':' + timeAfterColon
    elif (hasAMPM and hasColon == False):
        if (hasPM):
            if int(re.split('p|P', time)[0].strip()) == 12:
                finalTime = '12:00'
            else:
                finalTime = str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
        else:
            finalTime = re.split('a|A', time)[0].strip() + ':00'
    else:
        finalTime = time

    return finalTime
    # print(isNan, hasAMPM, hasColon, time, finalTime)

for day in days_list:
    # meals_both - split on the ampersand
    meals_both = meals[day].str.split('&', n=1, expand=True)

    meals_first = meals_both[0].str.split('-', n=1, expand=True)
    meals_second = meals_both[1].str.split('-', n=1, expand=True)

    meals_first_start = pd.Series()    
    for count, time in enumerate(meals_first[0]):
        meals_first_start[count] = checkAll(time)

    meals_first_end = pd.Series()
    for count, time in enumerate(meals_first[1]):
        meals_first_end[count] = checkAll(time)

    meals_second_start = pd.Series()
    for count, time in enumerate(meals_second[0]):
        meals_second_start[count] = checkAll(time)
    # meals_second_start = meals_second[0]

    meals_second_end = pd.Series()
    for count, time in enumerate(meals_second[1]):
        meals_second_end[count] = checkAll(time)
    # meals_second_end = meals_second[1]

    meals[day+'_start1']=meals_first_start
    meals[day+'_end1']=meals_first_end
    meals[day+'_start2']=meals_second_start
    meals[day+'_end2']=meals_second_end

meals.to_csv(OUTPUT_FILE)