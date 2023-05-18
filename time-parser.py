import pandas as pd

import os
from dotenv import load_dotenv
from pathlib import Path
import re

load_dotenv()

INPUT_FILE = os.getenv('INPUT_FILE')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')
# print(INPUT_FILE)

meals = pd.read_csv(INPUT_FILE)

days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def checkNan(value):
    if pd.isna(value):
        return True
    else:
        return False

def checkAMPM(value):
    allValues = ['AM', 'PM', 'am', 'pm', 'a.m.', 'p.m.', 'A.M.', 'P.M.']
    if checkNan(value) == False:
        if any(x in value for x in allValues):
            return True
        else:
            return False
    else:
        return False
    
def checkPM(value):
    allValues = ['PM', 'pm', 'p.m.', 'P.M.']
    if checkNan(value) == False:
        if any(x in value for x in allValues):
            return True
        else:
            return False
    else:
        return False
    
def checkColon(value):
    if checkNan(value) == False:
        if ':' in value:
            return True
        else:
            return False
    else:
        return False

def hasAMPMAndColon(time):
    print('hasAMPMAndColon, time: ', time)
    hasPM = checkPM(time.strip())
    timeBeforeColon = time.split(':')[0].strip()
    timeAfterColonWithAMPM = time.split(':')[1]
    timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    if (hasPM):
        if int(timeBeforeColon) == 12:
            return '12:' + timeAfterColon
        else:
            return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    else:
        return timeBeforeColon + ':' + timeAfterColon
    
def hasEndAMPMAndColon(time, endTime):
    print('hasEndAMPMAndColon, time: ', time)
    hasPM = checkPM(endTime.strip())
    timeBeforeColon = time.split(':')[0].strip()
    timeAfterColonWithAMPM = time.split(':')[1]
    timeAfterColon = re.split('a|A|p|P', timeAfterColonWithAMPM)[0].strip()
    if (hasPM):
        if int(timeBeforeColon) == 12:
            return '12:' + timeAfterColon
        else:
            return str(int(timeBeforeColon) + 12) + ':' + timeAfterColon
    else:
        return timeBeforeColon + ':' + timeAfterColon

def hasAMPMAndNoColon(time):
    hasPM = checkPM(time)
    if (hasPM):
        if int(re.split('p|P', time)[0].strip()) == 12:
            return '12:00'
        else:
            return str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
    else:
        return re.split('a|A', time)[0].strip() + ':00'
    
def hasEndAMPMAndNoColon(time, endTime):
    hasEndPM = checkPM(endTime)
    if (hasEndPM):
        if int(re.split('p|P', time)[0].strip()) == 12:
            return '12:00'
        else:
            return str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
    else:
        return re.split('a|A', time)[0].strip() + ':00'

def checkAll(time):
    parsedTimes = pd.Series()
    isNan = checkNan(time)

    if (isNan):
        parsedTimes[0] = ''
        parsedTimes[1] = ''
    else:
        startAndEnd = time.split('-')
        startHasAMPM = checkAMPM(startAndEnd[0])
        startHasColon = checkColon(startAndEnd[0])
        endHasAMPM = checkAMPM(startAndEnd[1])
        endHasColon = checkColon(startAndEnd[1])

        if (startHasAMPM and startHasColon):
            parsedTimes[0] = hasAMPMAndColon(startAndEnd[0])
        elif (startHasAMPM and startHasColon == False):
            parsedTimes[0] = hasAMPMAndNoColon(startAndEnd[0])
        elif (startHasAMPM == False and endHasAMPM and startHasColon):
            parsedTimes[0] = hasEndAMPMAndColon(startAndEnd[0], startAndEnd[1])
        elif (startHasAMPM == False and endHasAMPM and startHasColon == False):
            parsedTimes[0] = hasEndAMPMAndNoColon(startAndEnd[0], startAndEnd[1])
        else:
            parsedTimes[0] = startAndEnd[0]
        
        if (endHasAMPM and endHasColon):
            parsedTimes[1] = hasAMPMAndColon(startAndEnd[1])
        elif (endHasAMPM and endHasColon == False):
            parsedTimes[1] = hasAMPMAndNoColon(startAndEnd[1])
        else:
            parsedTimes[1] = startAndEnd[1]

    return parsedTimes

for day in days_list:
    meals_both = meals[day].str.split('&', n=1, expand=True)

    # meals_first = meals_both[0].str.split('-', n=1, expand=True)
    # meals_second = meals_both[1].str.split('-', n=1, expand=True)

    meals_first_parsed = pd.Series()    
    for count, time in enumerate(meals_both[0]):
        meals_first_parsed[count] = checkAll(time)
    meals_first_parsed_start = pd.Series()
    meals_first_parsed_end = pd.Series()
    for count, time in enumerate(meals_first_parsed):
        meals_first_parsed_start[count] = time[0]
        meals_first_parsed_end[count] = time[1]

    meals_second_parsed = pd.Series()    
    for count, time in enumerate(meals_both[1]):
        meals_second_parsed[count] = checkAll(time)
    meals_second_parsed_start = pd.Series()
    meals_second_parsed_end = pd.Series()
    for count, time in enumerate(meals_second_parsed):
        meals_second_parsed_start[count] = time[0]
        meals_second_parsed_end[count] = time[1]

    meals[day+'_start1']=meals_first_parsed_start
    meals[day+'_end1']=meals_first_parsed_end
    meals[day+'_start2']=meals_second_parsed_start
    meals[day+'_end2']=meals_second_parsed_end

meals.to_csv(OUTPUT_FILE)