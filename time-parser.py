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
    hasPM = checkPM(endTime)
    if (hasPM):
        if int(re.split('p|P', time)[0].strip()) == 12:
            return '12:00'
        else:
            return str(int(re.split('p|P', time)[0].strip()) + 12) + ':00'
    else:
        return re.split('a|A', time)[0].strip() + ':00'

def checkAll(time):
    finalTimes = pd.Series()
    isNan = checkNan(time)

    if (isNan):
        finalTimes[0] = ''
        finalTimes[1] = ''
    else:
        newTime = time.split('-')
        startHasAMPM = checkAMPM(newTime[0])
        # startHasPM = checkPM(newTime[0])
        startHasColon = checkColon(newTime[0])
        endHasAMPM = checkAMPM(newTime[1])
        # endHasPM = checkPM(newTime[1])
        endHasColon = checkColon(newTime[1])

        if (startHasAMPM and startHasColon):
            finalTimes[0] = hasAMPMAndColon(newTime[0])
        elif (startHasAMPM and startHasColon == False):
            finalTimes[0] = hasAMPMAndNoColon(newTime[0])
        elif (startHasAMPM == False and endHasAMPM and startHasColon):
            finalTimes[0] = hasEndAMPMAndColon(newTime[0], newTime[1])
        elif (startHasAMPM == False and endHasAMPM and startHasColon == False):
            finalTimes[0] = hasEndAMPMAndNoColon(newTime[0], newTime[1])
        else:
            finalTimes[0] = newTime[0]
        
        if (endHasAMPM and endHasColon):
            finalTimes[1] = hasAMPMAndColon(newTime[1])
        elif (endHasAMPM and endHasColon == False):
            finalTimes[1] = hasAMPMAndNoColon(newTime[1])
        else:
            finalTimes[1] = newTime[1]

    return finalTimes

for day in days_list:
    meals_both = meals[day].str.split('&', n=1, expand=True)

    meals_first = meals_both[0].str.split('-', n=1, expand=True)
    meals_second = meals_both[1].str.split('-', n=1, expand=True)

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